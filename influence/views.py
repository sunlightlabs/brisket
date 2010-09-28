# coding=utf-8

import urllib, re, datetime
import api, external_sites
from api               import DEFAULT_CYCLE
from django.http       import HttpResponseRedirect, HttpResponse
from django.shortcuts  import render_to_response
from django.template   import RequestContext
from influence.forms   import SearchForm, ElectionCycle
from influence.helpers import *
from operator          import itemgetter
from settings          import LATEST_CYCLE
from util              import catcodes
try:
    import json
except:
    import simplejson as json


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
        HttpResponseRedirect('/')

    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():
        kwargs = {}
        query = submitted_form.cleaned_data['query'].strip()
        cycle = request.GET.get('cycle', DEFAULT_CYCLE)
        
        # see ticket #545
        query = query.replace(u"’", "'")
                
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
            return HttpResponseRedirect('/%s/%s/%s%s' % (result_type, name, _id, "?cycle=" + cycle if cycle != "-1" else ""))

        kwargs['query'] = query

        if len(entity_results) == 0:
            kwargs['sorted_results'] = None
        else:
            # sort the results by type
            sorted_results = {'organization': [], 'politician': [], 'individual': [], 'lobbying_firm': [], 'industry': []}
            for result in entity_results:
                if result['type'] == 'organization' and result['lobbying_firm'] == True:
                    sorted_results['lobbying_firm'].append(result)
                else:
                    sorted_results[result['type']].append(result)

            # sort each type by amount
            sorted_results['industry']      = sorted(sorted_results['industry'],      key=lambda x: float(x['total_given']), reverse=True)
            sorted_results['organization']  = sorted(sorted_results['organization'],  key=lambda x: float(x['total_given']), reverse=True)
            sorted_results['individual']    = sorted(sorted_results['individual'],    key=lambda x: float(x['total_given']), reverse=True)
            sorted_results['politician']    = sorted(sorted_results['politician'],    key=lambda x: float(x['total_received']), reverse=True)
            sorted_results['lobbying_firm'] = sorted(sorted_results['lobbying_firm'], key=lambda x: float(x['firm_income']), reverse=True)

            # keep track of how many there are of each type of result
            kwargs['num_industries']   = len(sorted_results['industry'])
            kwargs['num_orgs']   = len(sorted_results['organization'])
            kwargs['num_pols']   = len(sorted_results['politician'])
            kwargs['num_indivs'] = len(sorted_results['individual'])
            kwargs['num_firms']  = len(sorted_results['lobbying_firm'])
            kwargs['cycle'] = cycle
            kwargs['sorted_results'] = sorted_results
        return render_to_response('results.html', kwargs, brisket_context(request))
    else:
        return HttpResponseRedirect('/')

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

def industry_landing(request):
    context = {}
    context['top_n_industries'] = api.top_n_industries(cycle=LATEST_CYCLE, limit=50)
    context['num_industries'] = len(context['top_n_industries'])
    context['cycle'] = LATEST_CYCLE
    return render_to_response('industry_landing.html', context, brisket_context(request))

def org_industry_entity(request, entity_id, type='organization'):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    context = {}
    context['entity_id'] = entity_id
    context['cycle'] = cycle

    metadata = get_metadata(entity_id, cycle, type)
    context['available_cycles'] = metadata['available_cycles']
    entity_info = metadata['entity_info']
    context['entity_info'] = entity_info
    
    # a little error-checking now that we have the entity info
    check_entity(entity_info, cycle, type)

    entity_info['metadata']['source_display_name'] = get_source_display_name(entity_info['metadata'])
    
    standardized_name = standardize_organization_name(entity_info['name']) if type == 'organization' else standardize_industry_name(entity_info['name'])
    
    context['external_links'] = external_sites.get_links(type, standardized_name, entity_info['external_ids'], cycle)
    
    if type == 'industry':
        context['top_orgs'] = json.dumps([
            {
                'key': generate_label(standardize_organization_name(org['organization_name'])),
                'value': org['amount'],
                'value_employee': org['amount'],
                'value_pac': 0,
                'href': '/organization/%s/%s%s' % (slugify(standardize_organization_name(org['organization_name'])), entity_id, '?cycle=%s' % cycle if cycle != '-1' else '')
            } for org in api.industry_orgs(entity_id, cycle, limit=10)
        ])

    # get contributions data if it exists for this entity
    if metadata['contributions']:
        context['contributions_data'] = True
        recipients = api.org_recipients(entity_id, cycle=cycle)

        recipients_barchart_data = []
        for record in recipients:
            recipients_barchart_data.append({
                    'key': generate_label(standardize_politician_name_with_metadata(record['name'], record['party'], record['state'])),
                    'value' : record['total_amount'],
                    'value_employee' : record['employee_amount'],
                    'value_pac' : record['direct_amount'],
                    'href' : barchart_href(record, cycle, entity_type='politician')
                    })
        context['recipients_barchart_data'] = json.dumps(bar_validate(recipients_barchart_data))

        party_breakdown = api.org_party_breakdown(entity_id, cycle)
        for key, values in party_breakdown.iteritems():
            party_breakdown[key] = float(values[1])
        context['party_breakdown'] = json.dumps(pie_validate(party_breakdown))

        level_breakdown = api.org_level_breakdown(entity_id, cycle)
        for key, values in level_breakdown.iteritems():
            level_breakdown[key] = float(values[1])
        context['level_breakdown'] = json.dumps(pie_validate(level_breakdown))

        # if none of the charts have data, or if the aggregate total
        # received was negative, then suppress that whole content
        # section except the overview bar
        if int(float(entity_info['totals']['contributor_amount'])) < 0:
            context['suppress_contrib_graphs'] = True
            context['reason'] = "negative"

        elif (not context['recipients_barchart_data']
              and not context['party_breakdown']
              and not context['level_breakdown']):
            context['suppress_contrib_graphs'] = True
            context['reason'] = 'empty'

        if cycle != DEFAULT_CYCLE:

            if int(cycle) == int(LATEST_CYCLE):
                cut_off_at_step = months_into_cycle_for_date(datetime.date.today(), cycle)
            else:
                cut_off_at_step = 24
        else:
            cut_off_at_step = 9999

        context['cut_off_sparkline_at_step'] = cut_off_at_step
        context['sparkline_data'] = api.org_sparkline_by_party(entity_id, cycle)

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
            context['lobbying_links'] = external_sites.get_lobbying_links('firm', standardize_organization_name(entity_info['name']), entity_info['external_ids'], cycle)
        else:
            context['lobbying_clients'] = api.org_registrants(entity_id, cycle)
            context['lobbying_lobbyists'] = api.org_lobbyists(entity_id, cycle)
            context['lobbying_issues'] =  [item['issue'] for item in api.org_issues(entity_id, cycle)]
            context['lobbying_links'] = external_sites.get_lobbying_links('client', standardize_organization_name(entity_info['name']), entity_info['external_ids'], cycle)


    return render_to_response('%s.html' % type, context,
                              entity_context(request, cycle, metadata['available_cycles']))

def organization_entity(request, entity_id):
    return org_industry_entity(request, entity_id, 'organization')

def industry_entity(request, entity_id):
    return org_industry_entity(request, entity_id, 'industry')


def politician_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    context = {}
    context['entity_id'] = entity_id
    context['cycle'] = cycle

    metadata = get_metadata(entity_id, cycle, "politician")
    context['available_cycles'] = metadata['available_cycles']
    entity_info = metadata['entity_info']
    
    # a little error-checking now that we have the entity info
    check_entity(entity_info, cycle, 'politician')

    entity_info['metadata']['source_display_name'] = get_source_display_name(entity_info['metadata'])

    context['external_links'] = external_sites.get_politician_links(standardize_politician_name(entity_info['name']), entity_info['external_ids'], cycle)

    context['entity_info'] = entity_info

    if metadata['contributions']:
        context['contributions_data'] = True

        top_contributors = api.pol_contributors(entity_id, cycle)
        top_industries = api.pol_industries(entity_id, cycle=cycle)

        contributors_barchart_data = []
        for record in top_contributors:
            contributors_barchart_data.append({
                'key': generate_label(standardize_organization_name(record['name'])),
                'value' : record['total_amount'],
                'value_employee' : record['employee_amount'],
                'value_pac' : record['direct_amount'],
                'href' : barchart_href(record, cycle, 'organization')
            })
        context['contributors_barchart_data'] = json.dumps(bar_validate(contributors_barchart_data))

        industries_barchart_data = []
        for record in top_industries:
            industries_barchart_data.append({
                'key': generate_label(record['industry']),
                'value' : record['amount'],
            })
        context['industries_barchart_data'] = json.dumps(bar_validate(industries_barchart_data))

        local_breakdown = api.pol_local_breakdown(entity_id, cycle)
        for key, values in local_breakdown.iteritems():
            # values is a list of [count, amount]
            local_breakdown[key] = float(values[1])
        context['local_breakdown'] = json.dumps(pie_validate(local_breakdown))

        entity_breakdown = api.pol_contributor_type_breakdown(entity_id, cycle)
        for key, values in entity_breakdown.iteritems():
            # values is a list of [count, amount]
            entity_breakdown[key] = float(values[1])
        context['entity_breakdown'] = json.dumps(pie_validate(entity_breakdown))

        # if none of the charts have data, or if the aggregate total
        # received was negative, then suppress that whole content
        # section except the overview bar
        if int(float(entity_info['totals']['recipient_amount'])) < 0:
            context['suppress_contrib_graphs'] = True
            context['reason'] = "negative"

        elif (not context['industries_barchart_data']
            and not context['contributors_barchart_data']
            and not context['local_breakdown']
            and not context['entity_breakdown']):
            context['suppress_contrib_graphs'] = True
            context['reason'] = 'empty'

        context['sparkline_data'] = api.pol_sparkline(entity_id, cycle)

    return render_to_response('politician.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))



def individual_entity(request, entity_id):
    cycle = request.GET.get('cycle', DEFAULT_CYCLE)
    context = {}
    context['entity_id'] = entity_id
    context['cycle'] = cycle

    # get entity metadata
    metadata = get_metadata(entity_id, cycle, "individual")
    available_cycles = metadata['available_cycles']
    entity_info = metadata['entity_info']
    
    # a little error-checking now that we have the entity info
    check_entity(entity_info, cycle, 'individual')

    context['entity_info'] = entity_info
    context['external_links'] = external_sites.get_individual_links(standardize_individual_name(entity_info['name']), entity_info['external_ids'], cycle)

    # get contributions information if it is available for this entity
    if metadata['contributions']:
        context['contributions_data'] = True
        recipient_candidates = api.indiv_pol_recipients(entity_id, cycle)
        recipient_orgs = api.indiv_org_recipients(entity_id, cycle)

        candidates_barchart_data = []
        for record in recipient_candidates:
            candidates_barchart_data.append({
                    'key': generate_label(standardize_politician_name_with_metadata(record['recipient_name'], record['party'], record['state'])),
                    'value' : record['amount'],
                    'href' : barchart_href(record, cycle, entity_type="politician"),
                    })
        context['candidates_barchart_data'] = json.dumps(bar_validate(candidates_barchart_data))

        orgs_barchart_data = []
        for record in recipient_orgs:
            orgs_barchart_data.append({
                    'key': generate_label(standardize_organization_name(record['recipient_name'])),
                    'value' : record['amount'],
                    'href' : barchart_href(record, cycle, entity_type="organization"),
                    })
        context['orgs_barchart_data'] = json.dumps(bar_validate(orgs_barchart_data))

        party_breakdown = api.indiv_party_breakdown(entity_id, cycle)
        for key, values in party_breakdown.iteritems():
            party_breakdown[key] = float(values[1])
        context['party_breakdown'] = json.dumps(pie_validate(party_breakdown))

        context['sparkline_data'] = api.indiv_sparkline(entity_id, cycle)

        # if none of the charts have data, or if the aggregate total
        # received was negative, then suppress that whole content
        # section except the overview bar
        if int(float(entity_info['totals']['contributor_amount'])) < 0:
            context['suppress_contrib_graphs'] = True
            context['reason'] = "negative"

        elif (not context['candidates_barchart_data']
            and not context['orgs_barchart_data']
            and not context['party_breakdown']):
            context['suppress_contrib_graphs'] = True
            context['reason'] = 'empty'


    # get lobbying info if it's available for this entity
    if metadata['lobbying']:
        context['lobbying_data'] = True
        context['lobbying_with_firm'] = api.indiv_registrants(entity_id, cycle)
        context['issues_lobbied_for'] =  [item['issue'] for item in api.indiv_issues(entity_id, cycle)]
        context['lobbying_for_clients'] = api.indiv_clients(entity_id, cycle)
        context['lobbying_links'] = external_sites.get_lobbying_links('lobbyist', standardize_individual_name(entity_info['name']), entity_info['external_ids'], cycle)

    return render_to_response('individual.html', context,
                              entity_context(request, cycle, available_cycles))


def get_source_display_name(metadata):
    source_display_names = {'wikipedia_info': 'Wikipedia', 'bioguide_info': 'Bioguide', 'sunlight_info': 'Sunlight'}
    return source_display_names.get(metadata.get('source_name', ''), '')


