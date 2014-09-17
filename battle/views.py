# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    data = {}

    if not request.user.is_anonymous():
        profile = request.user.get_profile()

        from battle.models import Warrior
        data['warriors'] = Warrior.objects.filter(summoner=profile)
        
        if not data['warriors'].exists():
            from battle.utils import get_friends, make_warriors
            raw = get_friends(profile.facebook_id, profile.access_token)
            
            import json
            make_warriors(json.loads(raw)['data'], profile)

    return render_to_response('index.html', data, context_instance=RequestContext(request))
