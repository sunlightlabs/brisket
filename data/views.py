from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
#from dcdata import contracts

#from locksmith.auth.models import ApiKey

# API_KEY = getattr(settings, 'SYSTEM_API_KEY', None)
# if not API_KEY:
#     raise ImproperlyConfigured("SYSTEM_API_KEY is a required parameter")

def index(request):
    return render_to_response('data/index.html', context_instance=RequestContext(request))

def filter(request):
    return HttpResponsePermanentRedirect('/contributions/')

def filter_contracts(request):
    return render_to_response('data/filter_contracts.html', context_instance=RequestContext(request))

def filter_contractor_misconduct(request):
    return render_to_response('data/filter_contractor_misconduct.html', context_instance=RequestContext(request))

def filter_epa_echo(request):
    return render_to_response('filter_epa_echo.html', context_instance=RequestContext(request))

def filter_faca(request):
    return render_to_response('filter_faca.html', context_instance=RequestContext(request))

def filter_contributions(request):
    return render_to_response('data/filter_contributions.html', context_instance=RequestContext(request))

def filter_bundling(request):
    return render_to_response('filter_bundling.html', context_instance=RequestContext(request))

def filter_earmarks(request):
    return render_to_response('data/filter_earmarks.html', context_instance=RequestContext(request))

def filter_grants(request):
    return render_to_response('data/filter_grants.html', context_instance=RequestContext(request))

def filter_lobbying(request):
    return render_to_response('data/filter_lobbying.html', context_instance=RequestContext(request))
        
def api_index(request):
    return render_to_response('data/api/index.html', context_instance=RequestContext(request))

def api_aggregate_contributions(request):
    return render_to_response('data/api/aggregates_contributions.html', context_instance=RequestContext(request))
    
def bulk_index(request):
    return render_to_response('data/bulk/index.html', context_instance=RequestContext(request))
        
def doc_index(request):
    return render_to_response('data/docs/index.html', context_instance=RequestContext(request))

#
# lookups documentation
#

def lookup(self, dataset, field):
    if dataset == 'contracts':
        attr = field.upper()
        if hasattr(contracts, attr):
            return render_to_response('docs/lookup.html', {
                'attr': attr,
                'lookup': getattr(contracts, attr),
            })
    raise Http404()


def search_count(request, search_resource):
    params = request.GET.copy()
    c = search_resource.handler.queryset(params).order_by().count() 
    return HttpResponse("%i" % c, content_type='text/plain')
    
    
def search_preview(request, search_resource):
    request.GET = request.GET.copy()
    request.GET['per_page'] = 30
    request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
    return search_resource(request)

    
def search_download(request, search_resource):
    request.GET = request.GET.copy()
    request.apikey = ApiKey.objects.get(key=API_KEY, status='A')
    request.GET['per_page'] = 1000000
    request.GET['format'] = 'xls'
    response = search_resource(request)
    response['Content-Disposition'] = "attachment; filename=%s.xls" % search_resource.handler.filename
    response['Content-Type'] = "application/vnd.ms-excel; charset=utf-8"
    return response

