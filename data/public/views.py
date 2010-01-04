from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import RequestContext
from dc_web.api.handlers import load_contributions, ContributionFilterHandler
from dc_web.api.urls import contributionfilter_handler

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def filter(request):
    return render_to_response('filter.html', context_instance=RequestContext(request))
        
def api_index(request):
    return render_to_response('api/index.html', context_instance=RequestContext(request))
    
def bulk_index(request):
    return render_to_response('bulk/index.html', context_instance=RequestContext(request))
        
def doc_index(request):
    return render_to_response('docs/index.html', context_instance=RequestContext(request))

#
# ajaxy stuff
#
def data_contributions(request):
    request.GET = request.GET.copy()
    request.GET['limit'] = 30
    request.GET['key'] = 'asdf'
    return contributionfilter_handler(request)
    
def data_contributions_download(request):
    request.GET = request.GET.copy()
    request.GET['key'] = 'asdf'
    request.GET['limit'] = 1000000
    request.GET['format'] = 'csv'
    return contributionfilter_handler(request)