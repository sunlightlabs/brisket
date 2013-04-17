# coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from settings import TOP_LISTS_CYCLE, api

def city_landing(request):
    context = {}
    return render_to_response('entity_landing/city_landing.html', context, RequestContext(request))

def state_landing(request):
    context = {}
    return render_to_response('entity_landing/state_landing.html', context, RequestContext(request))