# Create your views here.

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import RequestContext

from brisket.influence.forms import SearchForm
from lib import AggregatesAPI, InfluenceNetworkBuilder

def index(request):    
    search_form = SearchForm()
    return render_to_response('index.html', {'form':search_form})

def search(request):
    print 'helloooooooooo'
    if not request.GET.get('query', None):
        print 'Form Error'
        self.HttpResponseRedirect('/')
    
    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        api = AggregatesAPI()
        results = api.entity_search(submitted_form.cleaned_data['query'])
        return render_to_response('results.html', {'results': results})
    else: 
        form = SearchForm(request.GET)
        return HttpResponseRedirect('/')

        
    
