# coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from settings import TOP_LISTS_CYCLE, api

### Groups
def organization_landing(request):
    context = {}
    context['top_n_organizations'] = api.entities.top_n_organizations(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_orgs'] = len(context['top_n_organizations'])
    context['cycle'] = TOP_LISTS_CYCLE
    return render_to_response('entity_landing/org_landing.html', context, RequestContext(request))

def industry_landing(request):
    context = {}
    context['top_n_industries'] = api.entities.top_n_industries(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_industries'] = len(context['top_n_industries'])
    context['cycle'] = TOP_LISTS_CYCLE
    return render_to_response('entity_landing/industry_landing.html', context, RequestContext(request))

def pol_group_landing(request):
    context = {}
    return render_to_response('entity_landing/pol_group_landing.html', context, RequestContext(request))

def lobbying_firm_landing(request):
    context = {}
    return render_to_response('entity_landing/lobbying_firm_landing.html', context, RequestContext(request))


### Places
def city_landing(request):
    context = {}
    return render_to_response('entity_landing/city_landing.html', context, RequestContext(request))

def state_landing(request):
    context = {}
    return render_to_response('entity_landing/state_landing.html', context, RequestContext(request))


### People
def contributor_landing(request):
    context = {}
    context['top_n_individuals'] = api.entities.top_n_individuals(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_indivs'] = len(context['top_n_individuals'])
    context['cycle'] = TOP_LISTS_CYCLE
    return render_to_response('entity_landing/contributor_landing.html', context, RequestContext(request))

def lobbyist_landing(request):
    context = {}
    return render_to_response('entity_landing/lobbyist_landing.html', context, RequestContext(request))

def politician_landing(request):
    context = {}
    context['top_n_politicians'] = api.entities.top_n_politicians(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_pols'] = len(context['top_n_politicians'])
    context['cycle'] = TOP_LISTS_CYCLE
    return render_to_response('entity_landing/pol_landing.html', context, RequestContext(request))