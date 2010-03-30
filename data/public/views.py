
from time import time

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import RequestContext
from dcapi.contributions.handlers import load_contributions, ContributionFilterHandler
from dcapi.contributions.urls import contributionfilter_handler
from dcentity.models import Entity, Normalization
from dcentity.queries import search_entities_by_name
from dcdata.utils.strings.normalizer import basic_normalizer
from locksmith.auth.models import ApiKey

entity_type_map = {
    'quick': ('politician','organization'),
    'contributor': ('individual','committee'),
    'recipient': ('politician','committee'),
    'organization': ('organization',),
    'committee': ('committee',),
}

role_map = {
    'organization': 'organization',
    'politician': 'recipient',
}

API_KEY = getattr(settings, 'SYSTEM_API_KEY', None)
if not API_KEY:
    raise ImproperlyConfigured("SYSTEM_API_KEY is a required parameter")

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def filter(request):
    data = { }
    entity_id = request.GET.get('entityId', None)
    if entity_id:
        e = Entity.objects.get(pk=entity_id)
        data['entity'] = {
            'id': e.id,
            'name': e.name,
            'role': role_map[e.type],
        }
    return render_to_response('filter.html', data, context_instance=RequestContext(request))
        
def api_index(request):
    return render_to_response('api/index.html', context_instance=RequestContext(request))
    
def bulk_index(request):
    return render_to_response('bulk/index.html', context_instance=RequestContext(request))
        
def doc_index(request):
    return render_to_response('docs/index.html', context_instance=RequestContext(request))

#
# ajaxy stuff
#

def data_entities(request, entity_type):
    
    types = entity_type_map.get(entity_type, [])
    name = request.GET.get('q', None)
    
    result = list(search_entities_by_name(name, types))
    
    return HttpResponse("%s,%s\n" % (e[0], e[1]) for e in result)

def debug_contributions(request):
    content = '\n'.join(data_contributions(request))
    return render_to_response('debug.html', {'content': content})

def data_contributions(request):
    request.GET = request.GET.copy()
    request.GET['per_page'] = 30
    request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
    return contributionfilter_handler(request)

def data_contributions_count(request):    
    params = request.GET.copy()
    c = load_contributions(params, nolimit=True).order_by().count()
    return HttpResponse("%i" % c, content_type='text/plain')
    
def data_contributions_download(request):
    request.GET = request.GET.copy()
    request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
    request.GET['per_page'] = 1000000
    request.GET['format'] = 'csv'
    response = contributionfilter_handler(request)
    response['Content-Disposition'] = "attachment; filename=contributions.csv"
    response['Content-Type'] = "text/csv; charset=utf-8"
    return response


