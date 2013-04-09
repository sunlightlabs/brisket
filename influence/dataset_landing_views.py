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
from influence.helpers import prepare_entity_view, generate_label, barchart_href, \
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

def campaign_finance_landing(request):
    context = {}
    return render_to_response('dataset_landing/campaign_finance_landing.html', context, RequestContext(request))

def lobbying_landing(request):
    context = {}
    return render_to_response('dataset_landing/lobbying_landing.html', context, RequestContext(request))

def regs_landing(request):
    context = {}
    return render_to_response('dataset_landing/regs_landing.html', context, RequestContext(request))

def fed_spending_landing(request):
    context = {}
    return render_to_response('dataset_landing/fed_spending_landing.html', context, RequestContext(request))

def contractor_misconduct_landing(request):
    context = {}
    return render_to_response('dataset_landing/contractor_misconduct_landing.html', context, RequestContext(request))

def epa_echo_landing(request):
    context = {}
    return render_to_response('dataset_landing/epa_echo_landing.html', context, RequestContext(request))

def faca_landing(request):
    context = {}
    return render_to_response('dataset_landing/faca_landing.html', context, RequestContext(request))