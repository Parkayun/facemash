# -*- coding:utf-8 -*-
def get_friends(fb_id, access_token):
    url = u'https://graph.facebook.com/' + str(fb_id) + '/friends?' \
        + u'fields=id,name,picture.type(square).width(1000).height(1000)&' \
        + u'access_token=' + access_token
    
    import requests
    res = requests.get(url)
    return res.content


def make_warriors(friends, summoner):
    from battle.models import Warrior

    for friend in friends:
        fb_id = friend['id']
        fb_image_url = friend['picture']['data']['url']
        try:
            warrior = Warrior.objects.get(fb_id=fb_id, summoner=summoner)
            if warrior.fb_image_url != fb_image_url:
                warrior.fb_image_url = fb_image_url
                warrior.save()
        except Warrior.DoesNotExist:
            Warrior.objects.create(fb_id=fb_id, fb_image_url=fb_image_url,   
                                   summoner=summoner)


def expected(a_score, b_score):
    import math
    return 1 / (1 + math.pow(10, (a_score - b_score) / 400))

def win(score, expected, k=24):
    return score + k * (1-expected)

def loss(score, expected, k=24):
    return score + k + (0-expected)
