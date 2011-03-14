# coding=utf-8

from django.contrib.humanize.templatetags.humanize import apnumber
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import pluralize, slugify
from django.utils.datastructures import SortedDict
from influence import external_sites
from influence.api import DEFAULT_CYCLE, api
from influence.forms import SearchForm, ElectionCycle
from influence.helpers import prepare_entity_view, generate_label, barchart_href, \
    bar_validate, pie_validate, months_into_cycle_for_date, \
    filter_bad_spending_descriptions, make_bill_link
from influence.names import standardize_organization_name, standardize_industry_name
from name_cleaver.name_cleaver import PoliticianNameCleaver
from settings import LATEST_CYCLE
import datetime
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

def org_industry_entity(request, entity_id, type):
    cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, type)
    
    if metadata['contributions']:
        amount = int(float(metadata['entity_info']['totals']['contributor_amount']))
        org_contribution_section(entity_id, cycle, amount, type, context)
    
    if metadata['lobbying']:
        is_lobbying_firm = bool(metadata['entity_info']['metadata'].get('lobbying_firm', False))
        org_lobbying_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'], is_lobbying_firm, context)

    if metadata['fed_spending']:
        org_spending_section(entity_id, standardized_name, cycle, context)
        
    if 'earmarks' in metadata and metadata['earmarks']:
        org_earmarks_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'], context)

    return render_to_response('%s.html' % type, context,
                              entity_context(request, cycle, metadata['available_cycles']))

def org_contribution_section(entity_id, cycle, amount, type, context):
    if type == 'industry':
        context['top_orgs'] = json.dumps([
            {
                'key': generate_label(standardize_organization_name(org['name'])),
                'value': org['total_amount'],
                'value_employee': org['employee_amount'],
                'value_pac': org['direct_amount'],
                'href' : barchart_href(org, cycle, 'organization')
            } for org in api.industry_orgs(entity_id, cycle, limit=10)
        ])
    
    context['contributions_data'] = True
    recipients = api.org_recipients(entity_id, cycle=cycle)

    recipients_barchart_data = []
    for record in recipients:
        recipients_barchart_data.append({
                'key': generate_label(str(PoliticianNameCleaver(record['name']).parse().plus_metadata(record['party'], record['state']))),
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
    if amount < 0:
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



def org_lobbying_section(entity_id, name, cycle, external_ids, is_lobbying_firm, context):        
    context['lobbying_data'] = True
    context['is_lobbying_firm'] = is_lobbying_firm

    if is_lobbying_firm:
        context['lobbying_clients'] = api.org_registrant_clients(entity_id, cycle)
        context['lobbying_lobbyists'] = api.org_registrant_lobbyists(entity_id, cycle)
        context['lobbying_issues'] =  [item['issue'] for item in
                                       api.org_registrant_issues(entity_id, cycle)]
        context['lobbying_bills'] = [ { 'bill': bill['bill_name'], 'link': make_bill_link(bill) } \
                for bill in api.org_registrant_bills(entity_id, cycle) ]
        context['lobbying_links'] = external_sites.get_lobbying_links('firm', name, external_ids, cycle)
    else:
        context['lobbying_clients'] = api.org_registrants(entity_id, cycle)
        context['lobbying_lobbyists'] = api.org_lobbyists(entity_id, cycle)
        context['lobbying_issues'] =  [item['issue'] for item in api.org_issues(entity_id, cycle)]
        context['lobbying_bills'] = [ { 'bill': bill['bill_name'], 'link': make_bill_link(bill) } \
                for bill in api.org_bills(entity_id, cycle) ]
        context['lobbying_links'] = external_sites.get_lobbying_links('industry' if type == 'industry' else 'client', name, external_ids, cycle)


def org_earmarks_section(entity_id, name, cycle, external_ids, context):
    context['earmarks'] = earmarks_table_data(entity_id, cycle)
    context['earmark_links'] = external_sites.get_earmark_links('organization', name, external_ids, cycle)


def org_spending_section(entity_id, name, cycle, context):
    spending = api.org_fed_spending(entity_id, cycle)

    filter_bad_spending_descriptions(spending)

    context['grants_and_contracts'] = spending
    context['gc_links'] = external_sites.get_gc_links(name, cycle)

    gc_found_things = []
    for gc_type in ['grant', 'contract', 'loan']:
        if '%s_count' % gc_type in context['entity_info']['totals']:
            gc_found_things.append('%s %s%s' % (
                apnumber(context['entity_info']['totals']['%s_count' % gc_type]),
                gc_type,
                pluralize(context['entity_info']['totals']['%s_count' % gc_type])
            ))

    context['gc_found_things'] = gc_found_things
        

def organization_entity(request, entity_id):
    return org_industry_entity(request, entity_id, 'organization')

def industry_entity(request, entity_id):
    return org_industry_entity(request, entity_id, 'industry')


def politician_entity(request, entity_id):
    cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, 'politician')

    if metadata['contributions']:
        amount = int(float(metadata['entity_info']['totals']['recipient_amount']))
        pol_contribution_section(entity_id, cycle, amount, context)
        
    if metadata['earmarks']:
        pol_earmarks_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'], context)

    return render_to_response('politician.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))

def pol_contribution_section(entity_id, cycle, amount, context):
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
            'key': generate_label(standardize_industry_name(record['name'])),
            'href': barchart_href(record, cycle, 'industry'),
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
    if amount < 0:
        context['suppress_contrib_graphs'] = True
        context['reason'] = "negative"

    elif (not context['industries_barchart_data']
        and not context['contributors_barchart_data']
        and not context['local_breakdown']
        and not context['entity_breakdown']):
        context['suppress_contrib_graphs'] = True
        context['reason'] = 'empty'

    context['sparkline_data'] = api.pol_sparkline(entity_id, cycle)


def earmarks_table_data(entity_id, cycle):
    rows = api.pol_earmarks(entity_id, cycle)
    for row in rows:
        for member in row['members']:
            member['name'] = str(PoliticianNameCleaver(member['name']).parse().plus_metadata(member['party'], member['state']))
            
    return rows


def pol_earmarks_section(entity_id, name, cycle, external_ids, context):
    context['earmarks'] = earmarks_table_data(entity_id, cycle)
    
    local_breakdown = api.pol_earmarks_local_breakdown(entity_id, cycle)
    local_breakdown = dict([(key, float(value[1])) for key, value in local_breakdown.iteritems()])

    context['earmark_links'] = external_sites.get_earmark_links('politician', name, external_ids, cycle)

    ordered_pie = SortedDict([(key, local_breakdown.get(key, 0)) for key in ['unknown', 'in-state', 'out-of-state']])
    context['earmarks_local'] = json.dumps(pie_validate(ordered_pie))


def individual_entity(request, entity_id):
    cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, 'individual')

    if metadata['contributions']:
        amount = int(float(metadata['entity_info']['totals']['contributor_amount']))
        indiv_contribution_section(entity_id, cycle, amount, context)

    if metadata['lobbying']:
        indiv_lobbying_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'], context)

    return render_to_response('individual.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))


def indiv_contribution_section(entity_id, cycle, amount, context):
    context['contributions_data'] = True
    recipient_candidates = api.indiv_pol_recipients(entity_id, cycle)
    recipient_orgs = api.indiv_org_recipients(entity_id, cycle)

    candidates_barchart_data = []
    for record in recipient_candidates:
        candidates_barchart_data.append({
                'key': generate_label(str(PoliticianNameCleaver(record['recipient_name']).parse().plus_metadata(record['party'], record['state']))),
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
    if amount < 0:
        context['suppress_contrib_graphs'] = True
        context['reason'] = "negative"

    elif (not context['candidates_barchart_data']
        and not context['orgs_barchart_data']
        and not context['party_breakdown']):
        context['suppress_contrib_graphs'] = True
        context['reason'] = 'empty'


def indiv_lobbying_section(entity_id, name, cycle, external_ids, context):
    context['lobbying_data'] = True
    context['lobbying_with_firm'] = api.indiv_registrants(entity_id, cycle)
    context['issues_lobbied_for'] =  [item['issue'] for item in api.indiv_issues(entity_id, cycle)]
    context['lobbying_for_clients'] = api.indiv_clients(entity_id, cycle)
    context['lobbying_links'] = external_sites.get_lobbying_links('lobbyist', name, external_ids, cycle)


