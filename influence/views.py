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
#from network import InfluenceNetwork
from api import *
from brisket.util import catcodes
import urllib

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
    if request.session.has_key('influence_network'):
        inf = request.session['influence_network']
        print inf.as_json()
        context_variables['network'] = inf.as_json()
    return RequestContext(request, context_variables)

def index(request):    
    return render_to_response('index.html', brisket_context(request))

def search(request):
    if not request.GET.get('query', None):
        print 'Form Error'
        HttpResponseRedirect('/')
    
    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        api = AggregatesAPI()
        results = api.entity_search(submitted_form.cleaned_data['query'])

        # limit the results to only those entities with an ID. 
        entity_results = [result for result in results if result['id']]

        sorted_results = {'organization': [], 'politician': [], 'individual': []}
        for result in entity_results:
            sorted_results[result['type']].append(result)
        return render_to_response('results.html', {'sorted_results': sorted_results}, 
                                  brisket_context(request))
    else: 
        form = SearchForm(request.GET)
        return HttpResponseRedirect('/')

def organization_entity(request, entity_id):
    #update_network(request, entity_id)
    cycle = request.GET.get("cycle", 2010)
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    org_recipients = api.org_recipients(entity_id, cycle=cycle)
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
    for key, values in level_breakdown.iteritems():
        level_breakdown[key] = float(values[1])

    # get lobbying info
    lobbying = LobbyingAPI()
    lobbying_data = lobbying.by_client(entity_info['name'], cycle)
    if lobbying_data:
        lobbying_totals_by_firm = lobbying_by_firm(lobbying_data)
        lobbying_totals_by_sector = lobbying_by_sector(lobbying_data)
        # compile the summary statement for lobbying (easier here than in
        # the template)
        items = []
        for t in lobbying_totals_by_sector:
            items.append("$"+str(t[1])+" on <a href=''>"+
                         catcodes.industry_area[t[0]][1].title()
                         +"</a> (<a href=''>"+catcodes.industry_area[t[0]][0].title()+"</a>) ")
        if len(items) > 1:
            last = items.pop()
            lobbying_summary_stmt = entity_info['name'] + ' spent ' + ', '.join(items)+' and '+last+'.'
        else:
            lobbying_summary_stmt = entity_info['name'] + ' spent '+items[0]+'.'
    else: lobbying_summary_stmt = lobbying_totals_by_firm = None

    # fake us some sparkline data
    amounts = [str(recipient['total_amount']) for recipient in org_recipients]
    sparkline = timeline_sparkline(amounts)
    return render_to_response('organization.html', 
                              {'entity_id': entity_id, 
                               'entity_info': entity_info,
                               'level_breakdown' : level_breakdown,
                               'party_breakdown' : party_breakdown,
                               'recipients_barchart_data': recipients_barchart_data,
                               'lobbying_summary_stmt': lobbying_summary_stmt,
                               'lobbying_by_firm': lobbying_totals_by_firm,
                               'sparkline': sparkline,
                               },
                              entity_context(request))

def politician_entity(request, entity_id):
    #update_network(request, entity_id)

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
                'key': catcodes.sector[record['sector_code']],
                #'key': record['sector_code'],
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

    # get top words spoken in congress by this legislator for this cycle
    capitol_words = get_capitol_words(entity_info['name'], cycle, 50)

    # fake sparkline data
    amounts = [str(contributor['total_amount']) for contributor in top_contributors]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('politician.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'top_contributors': top_contributors,
                               'local_breakdown' : local_breakdown,
                               'entity_breakdown' : entity_breakdown,
                               'capitol_words': capitol_words,
                               'sectors_barchart_data': sectors_barchart_data,
                               'sparkline': sparkline,
                               },
                              entity_context(request))
        
def individual_entity(request, entity_id):    
    #update_network(request, entity_id)

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
    max_value = max([float(item) for item in data_list])
    scaling = "&chds=0,%f" % max_value
    data = "&chd=t:%s" % ','.join(data_list)
    url = "http://chart.apis.google.com/chart?cht=ls&chs=100x30"+data+scaling
    return url


# lobbying

def lobbying_by_sector(lobbying_data):
    amt_by_sector = {}
    for transaction in lobbying_data:
        sector = transaction['client_category']
        amount = transaction['amount']
        amt_by_sector[sector] = amt_by_sector.get(sector, 0) + int(float(amount))
    # sort and return as list of (firm, amt) tuples
    z = zip(amt_by_sector.keys(), amt_by_sector.values())
    z.sort(_tuple_cmp, reverse=True) # stupid in place sorting
    return z

def lobbying_by_firm(lobbying_data):
    amt_by_firm = {}
    for transaction in lobbying_data:
        if not transaction['registrant_is_firm']:
            continue
        firm = transaction['registrant_name']
        amount = transaction['amount']
        amt_by_firm[firm] = amt_by_firm.get(firm, 0) + int(float(amount))
    # sort and return as list of (firm, amt) tuples
    z = zip(amt_by_firm.keys(), amt_by_firm.values())
    z.sort(_tuple_cmp, reverse=True) # stupid in place sorting
    return z

def _tuple_cmp(t1, t2):
    ''' a cmp function for sort(), to sort tuples by increasing value
    of the tuple's 2nd item (index 1)'''
    if t1[1] < t2[1]:
        return -1
    if t1[1] > t2[1]:
        return 1
    else: return 0


# influence network functions

def update_network(request, entity_id):
    ''' Add the new entity to the Influence Network'''
    new_id = entity_id
    #weight = request.GET.get('weight')
    inf = request.session.get('influence_network', InfluenceNetwork())
    inf.add(new_id)
    request.session['influence_network'] = inf
    return 


def clear_network(request):
    if request.session.has_key('influence_network'):
        del request.session['influence_network']
    return HttpResponseRedirect('/')
