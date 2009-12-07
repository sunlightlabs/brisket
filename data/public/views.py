from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import RequestContext

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

# @login_required
# def account(request):
#     data = {
#         'profile': request.user.get_profile(),
#     }
#     return render_to_response('account/index.html', data, context_instance=RequestContext(request))
        
def api_index(request):
    return render_to_response('api/index.html', context_instance=RequestContext(request))
    
def bulk_index(request):
    return render_to_response('bulk/index.html', context_instance=RequestContext(request))