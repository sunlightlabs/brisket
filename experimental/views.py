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
from brisket.influence.forms import SearchForm, ElectionCycle
from lib import AggregatesAPI, InfluenceNetworkBuilder
import urllib, os
#import networkx as nx
try:
    import json
except:
    import simplejson as json


# FOR EXPERIMENTAL ONLY! anything served via a view from this file
# will look here for it's template files, without having to manually
# change the urls for every template file.
#settings.TEMPLATE_DIRS = (
#    os.path.join(settings.PROJECT_ROOT, 'templates/experimental'),
#)


class InfluenceNetwork(object):
    def __init__(self):
        self.network = nx.DiGraph()
        self.current_entity = None

    def add(self, entity_id, weight=None):
        # add a node for this entty, and an edge between this entity
        # and the previous (current) entity. then mark this entity as
        # the current entity. 
        
        # don't allow paths from the entity to itself
        if self.current_entity == entity_id:
            return
        self.network.add_node(str(entity_id))
        if self.current_entity:
            self.network.add_edge(str(self.current_entity), str(entity_id), weight)            
        self.current_entity = str(entity_id)        
        # eventually use an actual entity object that stores more info
        # about each entity.

    def as_json(self):
        ''' dumps node and edge names to json'''
        js = {}
        js['nodes'] = self.network.nodes()
        js['edges'] = self.network.edges()
        return json.dumps(js)

def brisket_context(request): 
    return RequestContext(request, {'search_form': SearchForm(), 
                                    })
def entity_context(request): 
    context_variables = {}    
    if request.GET.get('query', None):
        context_variables['search_form'] = SearchForm(request.GET)
    else:
        context_variables['search_form'] = SearchForm() 
    if request.GET.get('cycle', None):
        context_variables['cycle_form'] = ElectionCycle(request.GET)
    else:
        context_variables['cycle_form'] = ElectionCycle()
    # does this need to be passed in manually or are session variables
    # available to the templates by default? (doesn't seem so). 
    print 'checking now...'
    if request.session.has_key('influence_network'):
        inf = request.session['influence_network']
        print inf.as_json()
        context_variables['network'] = inf.as_json()
    else: print 'no network found'    
    return RequestContext(request, context_variables)

def index(request):    
    return render_to_response('index.html', brisket_context(request))

def graph_clear(request):
    if request.session.has_key('influence_network'):
        del request.session['influence_network']
    return HttpResponseRedirect('/experimental/graph')

def graph_test(request):    
    if request.GET.has_key('new_entity'):
        print 'new_entity'
        # add the new entity to the Influence Network
        new_id = request.GET.get('id')
        weight = request.GET.get('weight')
        inf = request.session.get('influence_network', InfluenceNetwork())
        inf.add(new_id, weight)
        print inf
        request.session['influence_network'] = inf
    return render_to_response('graph.html', entity_context(request))


def search(request):
    print 'experimental search'
    if not request.GET.get('query', None):
        print 'Form Error'
        HttpResponseRedirect('/experimental')

    if request.GET.get('new_entity', None):
        # add the new entity to the Influence Network
        new_id = request.GET.get('id')
        new_type = request.GET.get('type')
        inf = request.session.get('influence_network', InfluenceNetwork())
        inf.add(new_id, new_type)
        request.session['influence_network'] = inf

    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        api = AggregatesAPI()
        results = api.entity_search(submitted_form.cleaned_data['query'])

        # limit the results to only those entities with an ID. 
        entity_results = [result for result in results if result['id']]

        sorted_results = {'organization': [], 'politician': [], 'individual': []}
        for result in entity_results:
            sorted_results[result['type']].append(result)
        print entity_results
        print sorted_results
        return render_to_response('results.html', {'sorted_results': sorted_results}, 
                                  brisket_context(request))
    else: 
        form = SearchForm(request.GET)
        return HttpResponseRedirect('/')

def organization_entity(request, entity_id):

    cycle = request.GET.get("cycle", 2010)
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    org_recipients = api.org_recipients(entity_id, cycle=cycle)
    #print org_recipients
    recipients_barchart_data = []
    for record in org_recipients:        
        recipients_barchart_data.append({
                'key': record['name'],
                'value' : record['total_amount'],
                # currently we only display politician recipients from
                # orgs. this should be changed if we start returning
                # org-to-org data.
                'href' : "/politician/%s" % record['id'],
                })

    party_breakdown = api.org_breakdown(entity_id, 'party', cycle)
    print party_breakdown
    for key, values in party_breakdown.iteritems():
        party_breakdown[key] = float(values[1])
    level_breakdown = api.org_breakdown(entity_id, 'level', cycle)
    print 'here!'
    print level_breakdown
    for key, values in level_breakdown.iteritems():
        level_breakdown[key] = float(values[1])

    # fake us some sparkline data
    amounts = [str(recipient['total_amount']) for recipient in org_recipients]
    sparkline = timeline_sparkline(amounts)
    return render_to_response('organization.html', 
                              {'entity_id': entity_id, 
                               'entity_info': entity_info,
                               'level_breakdown' : level_breakdown,
                               'party_breakdown' : party_breakdown,
                               'recipients_barchart_data': recipients_barchart_data,
                               'sparkline': sparkline,
                               },
                              entity_context(request))

def politician_entity(request, entity_id):

    #check to see if a specific election cycle was specified, using
    #2010 as default if not.
    cycle = request.GET.get("cycle", 2010)
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    top_contributors = api.pol_contributors(entity_id, 'org', cycle=cycle)

    # top sectors is already sorted
    top_sectors = api.top_sectors(entity_id, cycle=cycle)
    sectors_barchart_data = []
    for record in top_sectors:        
        sectors_barchart_data.append({
                'key': record['sector_code'],
                'value' : record['amount'],
                'href' : "/industry/%s" % record['sector_code'],
                })

    local_breakdown = api.pol_breakdown(entity_id, 'local', cycle)
    for key, values in local_breakdown.iteritems():
        # values is a list of [count, amount]
        local_breakdown[key] = float(values[1])

    entity_breakdown = api.pol_breakdown(entity_id, 'entity', cycle)
    for key, values in entity_breakdown.iteritems():
        # values is a list of [count, amount]
        entity_breakdown[key] = float(values[1])    

    # fake sparkline data
    amounts = [str(contributor['total_amount']) for contributor in top_contributors]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('politician.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'top_contributors': top_contributors,
                               'local_breakdown' : local_breakdown,
                               'entity_breakdown' : entity_breakdown,
                               'sectors_barchart_data': sectors_barchart_data,
                               'sparkline': sparkline,
                               },
                              entity_context(request))
        
def individual_entity(request, entity_id):    
    # individuals only give contributions
    api = AggregatesAPI() 
    entity_info = api.entity_metadata(entity_id)    
    cycle = request.GET.get("cycle", 2010)

    recipient_candidates = api.indiv_recipients(entity_id, cycle=cycle, recipient_types='pol')
    candidates_barchart_data = []
    for record in recipient_candidates:        
        candidates_barchart_data.append({
                'key': record['name'],
                'value' : record['amount'],
                'href' : "/politician/%s" % record['id'],
                })

    recipient_orgs = api.indiv_recipients(entity_id, cycle=cycle, recipient_types='org')
    orgs_barchart_data = []
    for record in recipient_orgs:        
        orgs_barchart_data.append({
                'key': record['name'],
                'value' : record['amount'],
                'href' : "/organization/%s" % record['id'],
                })

    party_breakdown = api.indiv_breakdown(entity_id, 'party', cycle)
    for key, values in party_breakdown.iteritems():
        # values is a list of [count, amount]
        party_breakdown[key] = values[1]    

    # fake sparkline data
    amounts = [str(contributor['amount']) for contributor in recipient_candidates]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('individual.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'candidates_barchart_data': candidates_barchart_data,
                               'orgs_barchart_data': orgs_barchart_data,
                               'party_breakdown' : party_breakdown, 
                               'sparkline': sparkline,                               
                               },
                              entity_context(request))

def industry_detail(request, entity_id):
    cycle = request.GET.get("cycle", 2010)    
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)    
    top_industries = api.top_industries(entity_id, cycle=cycle)

    sectors = {}
    for industry in top_industries:
        industry_id = industry['category_name']        
        results = api.contributions_by_sector(entity_id, industry_id)
        sectors[industry_id] = (results)

    return render_to_response('industry_detail.html',
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'sectors': sectors,
                               },
                              entity_context(request))

def timeline_sparkline(data_list):
    ''' generates a sparkline of contributions given or received over
    the time period represented by the '''
    if not len(data_list):
        return None
    print 'sparkline data'
    print data_list
    max_value = max([float(item) for item in data_list])
    scaling = "&chds=0,%f" % max_value
    data = "&chd=t:%s" % ','.join(data_list)
    url = "http://chart.apis.google.com/chart?cht=ls&chs=100x30"+data+scaling
    return url

def raphael_demo(request):
    entity_id = "72dff1d2eacd4bf59283051f36ac4b61"
    api = AggregatesAPI()
    top_industries = api.top_sectors(entity_id, cycle='2008')
    fake_data = {'label1': 77, 'label2': 23}
    return render_to_response('chart_demo.html',
                              {'data': fake_data,
                               'bar_data': top_industries,
                               },
                              entity_context(request))

def rtest(request):
    return render_to_response('rtest.html')

