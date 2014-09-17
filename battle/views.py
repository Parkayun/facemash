# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    print request.user, dir(request.user)
    return render_to_response('index.html', context_instance=RequestContext(request))
