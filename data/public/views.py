from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from dcapi.contributions.handlers import load_contributions
from dcapi.contributions.urls import contributionfilter_handler
from dcapi.lobbying.handlers import load_lobbying
from dcapi.lobbying.urls import lobbyingfilter_handler
from locksmith.auth.models import ApiKey

API_KEY = getattr(settings, 'SYSTEM_API_KEY', None)
if not API_KEY:
    raise ImproperlyConfigured("SYSTEM_API_KEY is a required parameter")

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def filter(request):
    return HttpResponsePermanentRedirect('/contributions/')

def filter_contributions(request):
    return render_to_response('filter_contributions.html', context_instance=RequestContext(request))

def filter_lobbying(request):
    return render_to_response('filter_lobbying.html', context_instance=RequestContext(request))
        
def api_index(request):
    return render_to_response('api/index.html', context_instance=RequestContext(request))

def api_aggregate_contributions(request):
    return render_to_response('api/aggregates_contributions.html', context_instance=RequestContext(request))
    
def bulk_index(request):
    return render_to_response('bulk/index.html', context_instance=RequestContext(request))
        
def doc_index(request):
    return render_to_response('docs/index.html', context_instance=RequestContext(request))

#
# ajaxy contributions stuff
#

def debug_contributions(request):
    content = '\n'.join(data_contributions(request))
    return render_to_response('debug.html', {'content': content})

def data_contributions(request, count=False):
    if count:
        print "count"
        params = request.GET.copy()
        c = load_contributions(params, nolimit=True).order_by().count()
        return HttpResponse("%i" % c, content_type='text/plain')
    else:
        print "no count"
        request.GET = request.GET.copy()
        request.GET['per_page'] = 30
        request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
        return contributionfilter_handler(request)
    
def data_contributions_download(request):
    request.GET = request.GET.copy()
    request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
    request.GET['per_page'] = 1000000
    request.GET['format'] = 'xls'
    response = contributionfilter_handler(request)
    response['Content-Disposition'] = "attachment; filename=contributions.xls"
    response['Content-Type'] = "application/vnd.ms-excel; charset=utf-8"
    return response

#
# ajaxy lobbying stuff
#

def debug_lobbying(request):
    content = '\n'.join(data_lobbying(request))
    return render_to_response('debug.html', {'content': content})

def data_lobbying(request, count=False):
    if count:
        params = request.GET.copy()
        c = load_lobbying(params, nolimit=True).order_by().count()
        return HttpResponse("%i" % c, content_type='text/plain')
    else:
        request.GET = request.GET.copy()
        request.GET['per_page'] = 30
        request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
        return lobbyingfilter_handler(request)

def data_lobbying_download(request):
    request.GET = request.GET.copy()
    request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
    request.GET['per_page'] = 1000000
    request.GET['format'] = 'xls'
    response = lobbyingfilter_handler(request)
    response['Content-Disposition'] = "attachment; filename=lobbying.xls"
    response['Content-Type'] = "application/vnd.ms-excel; charset=utf-8"
    return response