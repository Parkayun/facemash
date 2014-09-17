# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    data = {}

    if not request.user.is_anonymous():
        profile = request.user.get_profile()

        from battle.utils import get_friends
        data['friends'] = get_friends(profile.facebook_id, profile.access_token)

    return render_to_response('index.html', data, context_instance=RequestContext(request))
