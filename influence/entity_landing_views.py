# coding=utf-8

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import pluralize, slugify
from django.utils.datastructures import SortedDict
from feedinator.models import Feed
from influence import external_sites
from influence.forms import SearchForm, ElectionCycle
from influence.helpers import generate_label, barchart_href, \
    bar_validate, pie_validate, \
    filter_bad_spending_descriptions, make_bill_link, get_top_pages
from influenceexplorer import DEFAULT_CYCLE
from influence.external_sites import _get_td_url
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver
from name_cleaver.names import PoliticianName
from settings import LATEST_CYCLE, TOP_LISTS_CYCLE, DOCKETWRENCH_URL, api
from urllib2 import URLError, HTTPError
import datetime
import json
import unicodedata

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