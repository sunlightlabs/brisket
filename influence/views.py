# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, re

from influence.forms import SearchForm, ElectionCycle
from influence import helpers
from util import catcodes
import api, external_sites
from api import DEFAULT_CYCLE
from settings import LATEST_CYCLE

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
        query = urllib.unquote(submitted_form.cleaned_data['query']).strip()
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

def organization_landing(request):
    context = {}
    context['top_n_organizations'] = api.top_n_organizations(cycle=LATEST_CYCLE, limit=50)
    context['num_orgs'] = len(context['top_n_organizations'])
    context['cycle'] = LATEST_CYCLE
    return render_to_response('org_landing.html', context, brisket_context(request))

def people_landing(request):
    context = {}
    context['top_n_individuals'] = api.top_n_individuals(cycle=LATEST_CYCLE, limit=50)
    context['num_indivs'] = len(context['top_n_individuals'])
    context['cycle'] = LATEST_CYCLE
    return render_to_response('indiv_landing.html', context, brisket_context(request))

def politician_landing(request):
    context = {}
    context['top_n_politicians'] = api.top_n_politicians(cycle=LATEST_CYCLE, limit=50)
    context['num_pols'] = len(context['top_n_politicians'])
    context['cycle'] = LATEST_CYCLE
    return render_to_response('pol_landing.html', context, brisket_context(request))

def organization_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    context = {}
    context['entity_id'] = entity_id
    context['cycle'] = cycle

    metadata = get_metadata(entity_id, cycle, "organization")
    context['available_cycles'] = metadata['available_cycles']
    entity_info = metadata['entity_info']
    context['external_links'] = external_sites.get_links(entity_info)
    context['entity_info'] = entity_info

    # get contributions data if it exists for this entity
    if metadata['contributions']:
        context['contributions_data'] = True
        org_recipients = api.org_recipients(entity_id, cycle=cycle)

        # check to see if some or all contributions are negative. if
        # they all are, don't display the charts. if only some are,
        # then remove them from the barchart.
        if float(entity_info['totals']['contributor_amount']) < 0:
            positive_recipients = [r for r in org_recipients if float(r['total_amount']) > 0.0]
            if len(positive_recipients) == 0:
                context['suppress_contrib_graphs'] = True
                print 'suppressing contribution charts because all data is negative'
            else:
                print 'removing some negative contributions from top contributors charts'
                org_recipients = positive_recipients

        recipients_barchart_data = []
        for record in org_recipients:
            recipients_barchart_data.append({
                    'key': _generate_label(helpers.standardize_politician_name(record['name'])),
                    'value' : record['total_amount'],
                    'href' : _barchart_href(record, cycle, entity_type='politician')
                    })
        context['recipients_barchart_data'] = validate(recipients_barchart_data)

        party_breakdown = api.org_party_breakdown(entity_id, cycle)
        for key, values in party_breakdown.iteritems():
            party_breakdown[key] = float(values[1])
        context['party_breakdown'] = party_breakdown

        level_breakdown = api.org_level_breakdown(entity_id, cycle)
        for key, values in level_breakdown.iteritems():
            level_breakdown[key] = float(values[1])
        context['level_breakdown'] = level_breakdown

        context['sparkline_data'] = api.org_sparkline(entity_id, cycle)

    # get lobbying info if it exists for this entity
    if metadata['lobbying']:
        context['lobbying_data'] = True
        is_lobbying_firm = bool(entity_info['metadata'].get('lobbying_firm', False))
        context['is_lobbying_firm'] = is_lobbying_firm

        if is_lobbying_firm:
            context['lobbying_clients'] = api.org_registrant_clients(entity_id, cycle)
            context['lobbying_lobbyists'] = api.org_registrant_lobbyists(entity_id, cycle)
            context['lobbying_issues'] =  [item['issue'] for item in
                                           api.org_registrant_issues(entity_id, cycle)]
        else:
            context['lobbying_clients'] = api.org_registrants(entity_id, cycle)
            context['lobbying_lobbyists'] = api.org_lobbyists(entity_id, cycle)
            context['lobbying_issues'] =  [item['issue'] for item in api.org_issues(entity_id, cycle)]

    return render_to_response('organization.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))


def politician_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    context = {}
    context['entity_id'] = entity_id
    context['cycle'] = cycle

    metadata = get_metadata(entity_id, cycle, "organization")
    context['available_cycles'] = metadata['available_cycles']
    entity_info = metadata['entity_info']
    context['external_links'] = external_sites.get_links(entity_info)
    context['entity_info'] = entity_info
    context['external_links'] = external_sites.get_links(entity_info)

    # check if the politician has a federal ID. we currently only have
    # politician metadata for federal politicians.
    for eid in entity_info['external_ids']:
        if eid['namespace'].find('urn:crp') >= 0:
            context['metadata'] = api.politician_meta(entity_info['name'])
            break

    if metadata['contributions']:
        context['contributions_data'] = True

        top_contributors = api.pol_contributors(entity_id, cycle)
        # check to see if some or all contributions are negative. if
        # they all are, don't display the charts. if only some are,
        # then remove them from the barchart.
        if float(entity_info['totals']['recipient_amount']) < 0:
            positive_contribs = [c for c in top_contributors if float(c['total_amount']) > 0.0]
            if len(positive_contribs) == 0:
                context['suppress_contrib_graphs'] = True
                print 'suppressing contribution charts because all data is negative'
            else:
                print 'removing some negative contributions from top contributors charts'
                top_contributors = positive_contribs

        contributors_barchart_data = []
        for record in top_contributors:
            contributors_barchart_data.append({
                    'key': _generate_label(record['name']),
                    'value' : record['total_amount'],
                    'value_employee' : record['employee_amount'],
                    'value_pac' : record['direct_amount'],
                    'href' : _barchart_href(record, cycle, 'organization')
                    })
        context['contributors_barchart_data'] = validate(contributors_barchart_data)

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
                    'href' : "-1" # will eventually link to industry pages.
                    })
        context['sectors_barchart_data'] = validate(sectors_barchart_data)

        local_breakdown = api.pol_local_breakdown(entity_id, cycle)
        for key, values in local_breakdown.iteritems():
            # values is a list of [count, amount]
            local_breakdown[key] = float(values[1])
        context['local_breakdown'] = local_breakdown

        entity_breakdown = api.pol_contributor_type_breakdown(entity_id, cycle)
        for key, values in entity_breakdown.iteritems():
            # values is a list of [count, amount]
            entity_breakdown[key] = float(values[1])
        context['entity_breakdown'] = entity_breakdown

        context['sparkline_data'] = api.pol_sparkline(entity_id, cycle)

    return render_to_response('politician.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))

def _barchart_href(record, cycle, entity_type):
    if 'recipient_entity' in record.keys():
        if record['recipient_entity']:
            href = str("/%s/%s/%s?cycle=%s" % (entity_type, slugify(record['recipient_name']),
                                               record['recipient_entity'], cycle))
        else:
            href = -1

    elif 'id' in record.keys():
        if record['id']:
            href = str("/%s/%s/%s?cycle=%s" % (entity_type, slugify(record['name']),
                                               record['id'], cycle))
        else:
            href = -1
    else:
        href = -1

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
    # check the metadata to see which of the fields are present. this
    # determines which sections to display on the entity page.
    section_indicators = {'individual': {'contributions': ('contributor_amount',),
                                         'lobbying': ('lobbying_count',)},
                          'organization' : {'contributions' : ('contributor_amount',),
                                            'lobbying': ('lobbying_count',)},
                          'politician' : {'contributions' : ('recipient_amount',)}
                          }

    entity_info = api.entity_metadata(entity_id, cycle)

    # check which types of data are available about this entity
    for data_type, indicators in section_indicators[entity_type].iteritems():
        if (entity_info['totals'].get(cycle, False) and
            [True for ind in indicators if entity_info['totals'][cycle][ind]]):
            data[data_type] = True
        else:
            data[data_type] = False


    data['available_cycles'] = entity_info['totals'].keys()
    # discard the info from cycles that are not the current one
    if entity_info['totals'].get(cycle, None):
        entity_info['totals'] = entity_info['totals'][cycle]
    data['entity_info'] = entity_info

    return data


def individual_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    context = {}
    context['entity_id'] = entity_id
    context['cycle'] = cycle

    # get entity metadata
    metadata = get_metadata(entity_id, cycle, "individual")
    available_cycles = metadata['available_cycles']
    entity_info = metadata['entity_info']

    context['external_links'] = external_sites.get_links(entity_info)
    context['entity_info'] = entity_info

    # get contributions information if it is available for this entity
    if metadata['contributions']:
        context['contributions_data'] = True
        recipient_candidates = api.indiv_pol_recipients(entity_id, cycle)
        recipient_orgs = api.indiv_org_recipients(entity_id, cycle)

        # check to see if some or all contributions are negative. if
        # they all are, don't display the charts. if only some are,
        # then remove them from the barchart.
        if float(entity_info['totals']['contributor_amount']) < 0:
            positive_cands = [r for r in recipient_candidates if float(r['amount']) > 0.0]
            positive_orgs = [r for r in recipient_orgs if float(r['amount']) > 0.0]
            if len(positive_cands) == 0 or len(positive_orgs) == 0:
                context['suppress_contrib_graphs'] = True
                print 'suppressing contribution charts because all data is negative'
            else:
                print 'removing some negative contributions from charts'
                recipient_candidates = positive_cands
                recipient_orgs = positive_orgs

        candidates_barchart_data = []
        for record in recipient_candidates:
            candidates_barchart_data.append({
                    'key': _generate_label(helpers.standardize_politician_name(record['recipient_name'])),
                    'value' : record['amount'],
                    'href' : _barchart_href(record, cycle, entity_type="politician"),
                    })
        context['candidates_barchart_data'] = validate(candidates_barchart_data)

        orgs_barchart_data = []
        for record in recipient_orgs:
            orgs_barchart_data.append({
                    'key': _generate_label(record['recipient_name']),
                    'value' : record['amount'],
                    'href' : _barchart_href(record, cycle, entity_type="organization"),
                    })
        context['orgs_barchart_data'] = validate(orgs_barchart_data)

        party_breakdown = api.indiv_party_breakdown(entity_id, cycle)
        for key, values in party_breakdown.iteritems():
            party_breakdown[key] = float(values[1])
        context['party_breakdown'] = party_breakdown

        context['sparkline_data'] = api.indiv_sparkline(entity_id, cycle)


    # get lobbying info if it's available for this entity
    if metadata['lobbying']:
        context['lobbying_data'] = True
        context['lobbying_with_firm'] = api.indiv_registrants(entity_id, cycle)
        context['issues_lobbied_for'] =  [item['issue'] for item in api.indiv_issues(entity_id, cycle)]
        context['lobbying_for_clients'] = api.indiv_clients(entity_id, cycle)

    return render_to_response('individual.html', context,
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

def validate(data):
    ''' take a dict formatted for submission to the barchart
     generation function, and make sure there's data worth displaying.
     if so, return the original data. if not, return false.'''
    print 'original data to be validated'
    print data

    # if all the data is 0 or if the list is empty, return false
    if sum([int(float(record['value'])) for record in data]) == 0:
        return False
    else:
        return data
    

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
