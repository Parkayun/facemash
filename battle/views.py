# -*- coding:utf-8 -*-
import json

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.db import transaction


def index(request):
    data = {}

    if not request.user.is_anonymous():
        profile = request.user.get_profile()
        data['summoner_id'] = profile.id

        from battle.models import Warrior
        warriors = Warrior.objects.filter(summoner=profile)
        
        if not warriors.exists():
            from battle.utils import get_friends, make_warriors
            raw = get_friends(profile.facebook_id, profile.access_token)
            
            make_warriors(json.loads(raw)['data'], profile)

        warriors = list(warriors)
        
        import random
        random.shuffle(warriors)
        
        data['warriors'] = warriors[:2]
        from battle.utils import expected
        data['expected'] = {
            'first': expected(warriors[0].score, warriors[1].score),
            'second': expected(warriors[1].score, warriors[0].score),
        }

        data['top10warriors'] = Warrior.objects.filter(summoner=profile).order_by('-wins')[:10]

    return render_to_response('index.html', data, context_instance=RequestContext(request))

@transaction.commit_on_success
def battle(request):
    result = {'status': 'error', 'message': ''}
    
    winner = request.GET.get('w', -1)
    loser = request.GET.get('l', -1)
    summoner = request.GET.get('s', -1)
    if winner == -1 or loser == -1 or summoner == -1:
        result['message'] = u'잘못된 배틀입니다.'

    try:
        from battle.models import Warrior
        winner = Warrior.objects.get(fb_id=winner, summoner_id=summoner)
        loser = Warrior.objects.get(fb_id=loser, summoner_id=summoner)
        
        from battle.utils import expected, win ,loss
        winner_expected = expected(loser.score, winner.score)
        winner_new_score = win(winner.score, winner_expected)
        winner.score = winner_new_score
        winner.wins += 1
        winner.save()
        
        loser_expected = expected(winner.score, loser.score)
        loser_new_score = loss(loser.score, loser_expected)
        loser.score = loser_new_score
        loser.losses += 1
        loser.save()

        warriors = list(Warrior.objects.all())
        
        import random
        random.shuffle(warriors)

        from battle.models import Battle
        Battle.objects.create(winner=winner, loser=loser, summoner_id=summoner)

        for idx, next_warrior in enumerate(warriors[:2]):
            next_warrior_data = next_warrior.get_all_summoner_data()
            result['next'+str(idx+1)] = {
                'fb_id': next_warrior.fb_id,
                'fb_image_url': next_warrior.fb_image_url,
                'score': next_warrior_data['score'],
                'wins': next_warrior_data['wins'],
                'losses': next_warrior_data['losses'],
                'expected': expected(next_warrior.score, winner.score)
            }

        result['status'] = 'success'

    except Warrior.DoesNotExist:
        result['message'] = u'잘못된 배틀입니다.'

    return HttpResponse(json.dumps(result),content_type='application/json')


def load_top10(request):
    summoner = request.GET.get('s', -1)
    
    from battle.models import Warrior
    
    tag = ''
    for warrior in Warrior.objects.filter(summoner_id=summoner).order_by('-wins')[:10]:
        data = warrior.get_all_summoner_data()
        tag += '<tr>'
        tag += '<td valign="top"><img src="'+warrior.fb_image_url+'" width="70" /></td>'
        tag += '<td valign="top">Score: '+str(data['score'])+'</td>'
        tag += '<td valign="top">Performance: '+str(warrior.get_performance())+'</td>'
        tag += '<td valign="top">Won: '+str(data['wins'])+'</td>'
        tag += '<td valign="top">Lost: '+str(data['losses'])+'</td>'
        tag += '</tr>'
    return HttpResponse(tag)
