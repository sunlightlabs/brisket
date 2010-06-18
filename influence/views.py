# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, re

from influence.forms import SearchForm, ElectionCycle
from util import catcodes
import api, external_sites
from api import DEFAULT_CYCLE

def brisket_context(request): 
    return RequestContext(request, {'search_form': SearchForm()})

def entity_context(request, cycle, available_cycles): 
    context_variables = {}    
    
    params = request.GET.copy()
    if 'cycle' not in params:
        params['cycle'] = DEFAULT_CYCLE

    context_variables['cycle_form'] = ElectionCycle(available_cycles, params)

    return RequestContext(request, context_variables)

def index(request):    
    return render_to_response('index.html', brisket_context(request))

def search(request):
    if not request.GET.get('query', None):
        print 'Form Error'
        HttpResponseRedirect('/')
    
    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        kwargs = {}
        query = urllib.unquote(submitted_form.cleaned_data['query'])
        cycle = request.GET.get('cycle', DEFAULT_CYCLE)

        # if a user submitted the search value from the form, then
        # treat the hyphens as intentional. if it was from a url, then
        # the name has probably been slug-ized and we need to remove
        # any single occurences of hyphens. 
        if not request.GET.get('from_form', None):            
            query = query.replace('-', ' ')
        results = api.entity_search(query)

        # limit the results to only those entities with an ID. 
        entity_results = [result for result in results if result['id']]

        # if there's just one results, redirect to that entity's page
        if len(entity_results) == 1:
            result_type = entity_results[0]['type']
            name = slugify(entity_results[0]['name'])
            _id = entity_results[0]['id']
            return HttpResponseRedirect('/%s/%s/%s?cycle=%s' % (result_type, name, _id, cycle))

        if len(entity_results) == 0:
            kwargs['sorted_results'] = None
        else:
            # sort the results by type
            sorted_results = {'organization': [], 'politician': [], 'individual': []}
            for result in entity_results:
                sorted_results[result['type']].append(result)

            # sort each type by amount
            sorted_results['organization'].sort(cmp=_amt_given_decreasing)
            sorted_results['individual'].sort(cmp=_amt_given_decreasing)
            sorted_results['politician'].sort(cmp=_amt_received_decreasing)

            # keep track of how many there are of each type of result
            kwargs['num_orgs'] = len(sorted_results['organization'])
            kwargs['num_pols'] = len(sorted_results['politician'])
            kwargs['num_indivs'] = len(sorted_results['individual'])
            kwargs['query'] = query
            kwargs['cycle'] = cycle
            kwargs['sorted_results'] = sorted_results
            print sorted_results
        return render_to_response('results.html', kwargs, brisket_context(request))
    else: 
        return HttpResponseRedirect('/')

def _amt_given_decreasing(d1, d2):
    ''' a cmp function for sort(), to sort dicts by increasing value
    of the total_given item'''

    if float(d1['total_given']) > float(d2['total_given']):
        return -1
    if float(d1['total_given']) < float(d2['total_given']):
        return 1
    else: return 0

def _amt_received_decreasing(d1, d2):
    ''' a cmp function for sort(), to sort dicts by increasing value
    of the total_given item'''

    if float(d1['total_received']) > float(d2['total_received']):
        return -1
    if float(d1['total_received']) < float(d2['total_received']):
        return 1
    else: return 0

def organization_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    entity_info = api.entity_metadata(entity_id, cycle)
    available_cycles = entity_info['totals'].keys()    
    # discard the info from cycles that are not the current one
    entity_info['totals'] = entity_info['totals'][cycle]
    external_links = external_sites.get_links(entity_info)

    org_recipients = api.org_recipients(entity_id, cycle=cycle)
    recipients_barchart_data = []
    for record in org_recipients:        
        recipients_barchart_data.append({
                'key': _generate_label(record['name']),
                'value' : record['total_amount'],
                'href' : str("/politician/%s/%s?cycle=%s" % (slugify(record['name']), record['id'], cycle)),
                })

    party_breakdown = api.org_party_breakdown(entity_id, cycle)
    for key, values in party_breakdown.iteritems():
        party_breakdown[key] = float(values[1])
    level_breakdown = api.org_level_breakdown(entity_id, cycle)
    for key, values in level_breakdown.iteritems():
        level_breakdown[key] = float(values[1])

    # sparkline data
    sparkline_data = api.org_sparkline(entity_id, cycle)
    print sparkline_data

    # get lobbying info
    try:
        is_lobbying_firm = entity_info['metadata']['lobbying_firm']
    except:
        is_lobbying_firm = False
    
    if is_lobbying_firm:
        lobbying_clients = api.org_registrant_clients(entity_id, cycle)
        lobbying_lobbyists = api.org_registrant_lobbyists(entity_id, cycle)
        lobbying_issues =  [item['issue'] for item in api.org_registrant_issues(entity_id, cycle)]
    else:
        lobbying_clients = api.org_registrants(entity_id, cycle)
        lobbying_lobbyists = api.org_lobbyists(entity_id, cycle)
        lobbying_issues =  [item['issue'] for item in api.org_issues(entity_id, cycle)]


    return render_to_response('organization.html', 
                              {'entity_id': entity_id, 
                               'entity_info': entity_info,
                               'level_breakdown' : level_breakdown,
                               'party_breakdown' : party_breakdown,
                               'recipients_barchart_data': recipients_barchart_data,
                               'sparkline_data': sparkline_data,
                               'external_links': external_links,
                               'cycle': cycle,
                               'is_lobbying_firm': is_lobbying_firm,
                               'lobbying_clients': lobbying_clients,
                               'lobbying_issues': lobbying_issues,
                               'lobbying_lobbyists': lobbying_lobbyists,
                               },
                              entity_context(request, cycle, available_cycles))

def politician_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)

    # metadata
    entity_info = api.entity_metadata(entity_id, cycle)
    available_cycles = entity_info['totals'].keys()
    # discard the info from cycles that are not the current one
    entity_info['totals'] = entity_info['totals'][cycle]
    external_links = external_sites.get_links(entity_info)

    # check if the politician has a federal ID. we currently only have
    # politician metadata for federal politicians.    
    for eid in entity_info['external_ids']:
        if eid['namespace'].find('urn:crp') >= 0:
            metadata = api.politician_meta(entity_info['name'])
            break
        else:
            metadata = None

    top_contributors = api.pol_contributors(entity_id, cycle)
    contributors_barchart_data = []
    for record in top_contributors:
        contributors_barchart_data.append({ 
                'key': _generate_label(record['name']),
                'value' : record['total_amount'],
                'value_employee' : record['employee_amount'],
                'value_pac' : record['direct_amount'],
                'href' : _barchart_href(record, cycle, 'organization')
                })

    # top sectors is already sorted
    top_sectors = api.pol_sectors(entity_id, cycle=cycle)
    sectors_barchart_data = []
    for record in top_sectors:        
        try:
            sector_name = catcodes.sector[record['sector']]
        except:
            sector_name = 'Unknown (%s)' % record['sector']
        sectors_barchart_data.append({                
                'key': _generate_label(sector_name),
                'value' : record['amount'],
                'href' : str("/sector/%s/%s?cycle=%s" % (slugify(sector_name), 
                                                         record['sector'], cycle)),
                })

    local_breakdown = api.pol_local_breakdown(entity_id, cycle)
    for key, values in local_breakdown.iteritems():
        # values is a list of [count, amount]
        local_breakdown[key] = float(values[1])

    entity_breakdown = api.pol_contributor_type_breakdown(entity_id, cycle)
    for key, values in entity_breakdown.iteritems():
        # values is a list of [count, amount]
        entity_breakdown[key] = float(values[1])    

    # sparkline data
    sparkline_data = api.pol_sparkline(entity_id, cycle)
    print sparkline_data

    return render_to_response('politician.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'top_contributors': top_contributors,
                               'local_breakdown' : local_breakdown,
                               'entity_breakdown' : entity_breakdown,
                               'metadata': metadata,
                               'sectors_barchart_data': sectors_barchart_data,
                               'contributors_barchart_data': contributors_barchart_data,
                               'sparkline_data': sparkline_data,
                               'external_links': external_links,
                               'cycle': cycle,
                               },
                              entity_context(request, cycle, available_cycles))

def _barchart_href(record, cycle, entity_type):
    if 'recipient_entity' in record.keys(): 
        if record['recipient_entity']:
            href = str("/%s/%s/%s?cycle=%s" % (entity_type, slugify(record['recipient_name']), 
                                               record['recipient_entity'], cycle))
        else:
            href = str("/search?query=%s&cycle=%s" % (record['recipient_name'], cycle))

    elif 'id' in record.keys(): 
        if record['id']:
            href = str("/%s/%s/%s?cycle=%s" % (entity_type, slugify(record['name']), 
                                               record['id'], cycle))
        else:
            href = str("/search?query=%s&cycle=%s" % (record['name'], cycle))

    return href
 
def _generate_label(string):
    ''' truncate names longer than max_length and normalize the case
    to use title case'''
    max_length = 27
    label = string[:max_length] + (lambda x, l: (len(x)>l and "...") 
                                   or "")(string, max_length)
    return label.title()


def get_metadata(entity_id, cycle, entity_type):
    ''' beginnings of some refactoring. half implemented but
    harmless. do not pet or feed.'''
    data = {}
    data_availability = {'individual': {'contributions': ('contributor_amount',)},
                       'politician' : {},
                       'organization' : {}
                       }

    entity_info = api.entity_metadata(entity_id, cycle)    

    # check which types of data are available about this entity
    for data_type, indicators in data_availability[entity_type].iteritems():
        if (entity_info['totals'].get(cycle, False) and 
            [True for ind in indicators if entity_info['totals'][cycle][ind]]):
            data[data_type] = True
        else:
            data[data_type] = False

    print data['contributions']

    data['available_cycles'] = entity_info['totals'].keys()    
    if entity_info['totals'].get(cycle, None):
        entity_info['totals'] = entity_info['totals'][cycle]
    data['entity_info'] = entity_info

    return data
    

def individual_entity(request, entity_id):    
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    cv = {}
    # get entity metadata
    metadata = get_metadata(entity_id, cycle, "individual")
    available_cycles = metadata['available_cycles']
    entity_info = metadata['entity_info']

    external_links = external_sites.get_links(entity_info)
    print 'external links'
    print external_links

    recipient_candidates = api.indiv_pol_recipients(entity_id, cycle)
    candidates_barchart_data = []
    for record in recipient_candidates:        
        candidates_barchart_data.append({
                'key': _generate_label(record['recipient_name']),
                'value' : record['amount'],
                'href' : _barchart_href(record, cycle, entity_type="politician"),
                })

    recipient_orgs = api.indiv_org_recipients(entity_id, cycle)
    orgs_barchart_data = []
    for record in recipient_orgs:        
        orgs_barchart_data.append({
                'key': _generate_label(record['recipient_name']),
                'value' : record['amount'],
                'href' : _barchart_href(record, cycle, entity_type="organization"),
                })

    party_breakdown = api.indiv_party_breakdown(entity_id, cycle)
    print 'party breakdown'
    print party_breakdown
    for key, values in party_breakdown.iteritems():
        party_breakdown[key] = float(values[1])

    # sparkline data
    sparkline_data = api.indiv_sparkline(entity_id, cycle)
    print sparkline_data

    # get lobbying info
    lobbying_with_firm = api.indiv_registrants(entity_id, cycle)
    issues_lobbied_for =  [item['issue'] for item in api.indiv_issues(entity_id, cycle)]
    lobbying_for_clients = api.indiv_clients(entity_id, cycle)    

    return render_to_response('individual.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'candidates_barchart_data': candidates_barchart_data,
                               'orgs_barchart_data': orgs_barchart_data,
                               'party_breakdown' : party_breakdown, 
                               'lobbying_with_firm': lobbying_with_firm,
                               'issues_lobbied_for': issues_lobbied_for,
                               'lobbying_for_clients': lobbying_for_clients,
                               'sparkline_data': sparkline_data,
                               'external_links': external_links,
                               'cycle': cycle,
                               },
                              entity_context(request, cycle, available_cycles))

def industry_detail(request, entity_id):
    cycle = request.GET.get("cycle", DEFAULT_CYCLE)    
    entity_info = api.entity_metadata(entity_id, cycle)    
    top_industries = api.pol_sectors(entity_id, cycle)

    sectors = {}
    for industry in top_industries:
        industry_id = industry['category_name']        
        results = api.org_industries_for_sector(entity_id, industry_id)
        sectors[industry_id] = (results)

    return render_to_response('industry_detail.html',
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'sectors': sectors,
                               },
                              entity_context(request, cycle))

# lobbying

def lobbying_by_industry(lobbying_data):
    ''' aggregates lobbying spending by industry'''
    amt_by_industry = {}
    for transaction in lobbying_data:
        industry = transaction['client_category']
        amount = transaction['amount']
        amt_by_industry[industry] = amt_by_industry.get(industry, 0) + int(float(amount))
    # sort into a list of (sector_code, amt) tuples
    z = zip(amt_by_industry.keys(), amt_by_industry.values())
    z.sort(_tuple_cmp, reverse=True)
    # add in the industry and area names
    # return tuples now contain (industry_code, industry_name, industry_area, amt)
    annotated = []
    for item in z:
        code = item[0]
        industry = catcodes.industry_area[item[0].upper()][0]
        sub_industry = catcodes.industry_area[item[0].upper()][1] 
        amount = item[1]
        annotated.append((code, industry, sub_industry, amount))
    return annotated

def lobbying_by_customer(lobbying_data):
    amt_by_customer = {}
    for transaction in lobbying_data:
        #if not transaction['registrant_is_firm']:
        #    continue
        customer = transaction['client_name']
        amount = transaction['amount']
        amt_by_customer[customer] = amt_by_customer.get(customer, 0) + int(float(amount))
    # sort and return as list of (firm, amt) tuples
    z = zip(amt_by_customer.keys(), amt_by_customer.values())
    z.sort(_tuple_cmp, reverse=True) 
    return z


def lobbying_by_firm(lobbying_data):
    amt_by_firm = {}
    for transaction in lobbying_data:
        #if not transaction['registrant_is_firm']:
        #    continue
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


def slugify(string):
    ''' like the django template tag, converts to lowercase, removes
    all non-alphanumeric characters and replaces spaces with
    hyphens. '''
    return re.sub(" ", "-", re.sub("[^a-zA-Z0-9 -]+", "", string)).lower()
