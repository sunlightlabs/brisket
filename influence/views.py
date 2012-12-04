# coding=utf-8

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import pluralize, slugify
from django.utils.datastructures import SortedDict
from feedinator.models import Feed
from influence import external_sites
from influence.forms import SearchForm, ElectionCycle
from influence.helpers import prepare_entity_view, generate_label, barchart_href, \
    bar_validate, pie_validate, \
    filter_bad_spending_descriptions, make_bill_link, get_top_pages, \
    standardize_name
from influenceexplorer import DEFAULT_CYCLE
from influence.external_sites import _get_td_url
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver
from settings import LATEST_CYCLE, TOP_LISTS_CYCLE, api
from urllib2 import URLError
import datetime
import json


# Exceptions need a functioning unicode method
# for Sentry. URLError and its subclass HTTPError
# do not. So monkey patching.
URLError.__unicode__ = lambda self: unicode(self.__str__())


def handle_errors(f):
    def wrapped_f(*args, **params):
        try:
            return f(*args, **params)
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                raise Http404
            raise

    return wrapped_f


def brisket_context(request):
    return RequestContext(request, {'search_form': SearchForm()})


def entity_context(request, cycle, available_cycles):
    context_variables = {}

    params = request.GET.copy()
    params['cycle'] = cycle

    context_variables['cycle_form'] = ElectionCycle(available_cycles, params)

    return RequestContext(request, context_variables)


def entity_redirect(request, entity_id):
    entity = api.entities.metadata(entity_id)

    name = slugify(entity['name'])

    return redirect('{}_entity'.format(entity['type']), entity_id=entity_id)


#this is the index
def index(request):
    #ID of the feed is hardcoded as feed 1 since it's the only feed we're using right now. This may change!
    feed = Feed.objects.get(pk=1)
    entry = feed.entries.values().latest('date_published')
    entry['title'] = entry['title'].replace('Influence Explored: ', '')
    return render_to_response('index.html', {"feed": feed, "entry": entry, "top_pages": get_top_pages()}, brisket_context(request))


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

        results = api.entities.search(query)

        # limit the results to only those entities with an ID.
        entity_results = [result for result in results if result['id']]

        # if there's just one results, redirect to that entity's page
        if len(entity_results) == 1:
            result_type = entity_results[0]['type']
            name = slugify(entity_results[0]['name'])
            _id = entity_results[0]['id']
            return HttpResponseRedirect('/%s/%s/%s%s' % (result_type, name, _id, "?cycle=" + cycle if cycle != "-1" else ""))

        kwargs['query'] = query
        kwargs['contributor_search_link'] = _get_td_url('individual', query, None, None)

        if len(entity_results) == 0:
            kwargs['sorted_results'] = None
        else:
            # sort the results by type
            sorted_results = {'organization': [], 'politician': [], 'individual': [], 'lobbying_firm': [], 'industry': [], 'superpac': []}
            for result in entity_results:
                if result['type'] == 'organization' and result['lobbying_firm'] == True:
                    sorted_results['lobbying_firm'].append(result)
                elif result['type'] == 'organization' and result['is_superpac'] == True:
                    sorted_results['superpac'].append(result)
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
            kwargs['num_superpacs'] = len(sorted_results['superpac'])
            kwargs['cycle'] = cycle
            kwargs['sorted_results'] = sorted_results
        return render_to_response('results.html', kwargs, brisket_context(request))
    else:
        return HttpResponseRedirect('/')

def organization_landing(request):
    context = {}
    context['top_n_organizations'] = api.entities.top_n_organizations(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_orgs'] = len(context['top_n_organizations'])
    context['cycle'] = TOP_LISTS_CYCLE

    context['top_indexp_pacs'] = translate_top_list_for_chart(api.entities.top_n_pacs_by_indexp(cycle=TOP_LISTS_CYCLE, limit=10), type_='organization')
    context['top_firms'] = translate_top_list_for_chart(api.entities.top_n_firms_by_income(cycle=TOP_LISTS_CYCLE, limit=10), type_='organization')
    context['top_lobbying_clients'] = translate_top_list_for_chart(api.entities.top_n_orgs_lobbying(cycle=TOP_LISTS_CYCLE, limit=10), type_='organization')
    context['top_state_pac_donors'] = translate_top_list_for_chart(api.entities.top_n_org_donors_by_area_contributor_type(cycle=TOP_LISTS_CYCLE, limit=10, area='state', contributor_type='pac'), type_='organization')
    context['top_state_employee_donors'] = translate_top_list_for_chart(api.entities.top_n_org_donors_by_area_contributor_type(cycle=TOP_LISTS_CYCLE, limit=10, area='state', contributor_type='employee'), type_='organization')
    context['top_federal_pac_donors'] = translate_top_list_for_chart(api.entities.top_n_org_donors_by_area_contributor_type(cycle=TOP_LISTS_CYCLE, limit=10, area='federal', contributor_type='pac'), type_='organization')
    context['top_federal_employee_donors'] = translate_top_list_for_chart(api.entities.top_n_org_donors_by_area_contributor_type(cycle=TOP_LISTS_CYCLE, limit=10, area='federal', contributor_type='employee'), type_='organization')

    context['top_regs_submitters'] = api.entities.top_n_regs_submitters(cycle=TOP_LISTS_CYCLE, limit=10)

    return render_to_response('org_landing.html', context, brisket_context(request))

def people_landing(request):
    context = {}
    context['top_n_individuals'] = api.entities.top_n_individuals(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_indivs'] = len(context['top_n_individuals'])
    context['cycle'] = TOP_LISTS_CYCLE

    democratic_donors = api.entities.top_n_indiv_democratic_donors(cycle=TOP_LISTS_CYCLE, limit=10)
    context['top_n_democratic_donors'] = translate_top_list_for_chart(democratic_donors)

    republican_donors = api.entities.top_n_indiv_republican_donors(cycle=TOP_LISTS_CYCLE, limit=10)
    context['top_n_republican_donors'] = translate_top_list_for_chart(republican_donors)

    lobbyist_bundlers = api.entities.top_n_lobbyist_bundlers(cycle=TOP_LISTS_CYCLE, limit=10)
    context['top_n_lobbyist_bundlers'] = translate_top_list_for_chart(lobbyist_bundlers)

    top_state_donors = api.entities.top_n_indivs_by_area(cycle=TOP_LISTS_CYCLE, limit=10, area='state')
    context['top_n_state_donors'] = translate_top_list_for_chart(top_state_donors)

    top_federal_donors = api.entities.top_n_indivs_by_area(cycle=TOP_LISTS_CYCLE, limit=10, area='federal')
    context['top_n_federal_donors'] = translate_top_list_for_chart(top_federal_donors)

    return render_to_response('indiv_landing.html', context, brisket_context(request))

def translate_top_list_for_chart(data, type_='individual'):
    name = lambda x: str(standardize_name(x['name'], type_)) if type_ == 'organization' else standardize_name(x['name'], type_).name_str()
    return json.dumps([ {
        'key': name(x),
        'href': '/{}/{}/{}?cycle={}'.format(type_, slugify(name(x)), x['entity_id'], TOP_LISTS_CYCLE),
        'value': x.get('amount', x.get('count'))
    } for x in data])

def translate_top_list_for_lg_donations_chart(data, type_='individual'):

    def parse_contributor_name(row):
        try:
            name = str(standardize_name(row['contributor_name'], 'individual'))
        except:
            name = str(standardize_name(row['contributor_name'], 'organization'))

        return name

    contrib_name = parse_contributor_name
    committee_name = lambda x: str(standardize_name(x['committee_name'], 'organization'))
    return json.dumps([ {
        'key': '{1} (from {0})'.format(contrib_name(x), committee_name(x)) if x['contributor_name'] else committee_name(x),
        'href': '/{}/{}/{}?cycle={}'.format('organization', slugify(committee_name(x)), x['committee_entity'], TOP_LISTS_CYCLE),
        'value': x.get('amount')
    } for x in data])

def translate_top_list_for_stacked_chart(data, amount_fields, type_='individual'):
    name = lambda x: str(standardize_name(x['name'], type_)) if type_ == 'organization' else standardize_name(x['name'], type_).name_str()
    return json.dumps([ {
        'name': name(x),
        'href': '/{}/{}/{}?cycle={}'.format(type_, slugify(name(x)), x['entity_id'], TOP_LISTS_CYCLE),
        'value_a': x.get(amount_fields[0]),
        'value_b': x.get(amount_fields[1])
    } for x in data])

def politician_landing(request):
    context = {}
    context['top_n_politicians'] = api.entities.top_n_politicians(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_pols'] = len(context['top_n_politicians'])
    context['cycle'] = TOP_LISTS_CYCLE

    context['largest_donations_in_last_month'] = translate_top_list_for_lg_donations_chart(api.entities.top_n_largest_donations_in_last_month(limit=10))

    context['top_by_receipts_for_house'] = translate_top_list_for_chart(api.entities.top_n_politicians(limit=10, office='house'), type_='politician')
    context['top_by_receipts_for_senate'] = translate_top_list_for_chart(api.entities.top_n_politicians(limit=10, office='senate'), type_='politician')
    context['top_by_receipts_for_president'] = translate_top_list_for_chart(api.entities.top_n_politicians(limit=10, office='president'), type_='politician')
    context['top_by_receipts_for_governor'] = translate_top_list_for_chart(api.entities.top_n_politicians(limit=10, office='governor'), type_='politician')

    context['top_by_indexp_for_house'] = translate_top_list_for_stacked_chart(api.entities.top_n_pols_by_indexp_by_office('house', limit=10), ['oppose_amount', 'support_amount'], type_='politician')
    context['top_by_indexp_for_senate'] = translate_top_list_for_stacked_chart(api.entities.top_n_pols_by_indexp_by_office('senate', limit=10), ['oppose_amount', 'support_amount'], type_='politician')
    context['top_by_indexp_for_president'] = translate_top_list_for_stacked_chart(api.entities.top_n_pols_by_indexp_by_office('president', limit=10), ['oppose_amount', 'support_amount'], type_='politician')

    return render_to_response('pol_landing.html', context, brisket_context(request))

def industry_landing(request):
    context = {}
    context['top_n_industries'] = api.entities.top_n_industries(cycle=TOP_LISTS_CYCLE, limit=50)
    context['num_industries'] = len(context['top_n_industries'])
    context['cycle'] = TOP_LISTS_CYCLE

    lobbying_industries = api.entities.top_n_orgs_lobbying(cycle=TOP_LISTS_CYCLE, limit=50, is_industry=True)
    context['top_lobbying_clients'] = translate_top_list_for_chart(lobbying_industries, type_='organization')

    democratic_industries = api.entities.top_n_industry_donors_to_democrats(cycle=TOP_LISTS_CYCLE, limit=10)
    context['top_donors_to_democrats'] = translate_top_list_for_chart(democratic_industries, type_='organization')

    republican_industries = api.entities.top_n_industry_donors_to_republicans(cycle=TOP_LISTS_CYCLE, limit=10)
    context['top_donors_to_republicans'] = translate_top_list_for_chart(republican_industries, type_='organization')

    return render_to_response('industry_landing.html', context, brisket_context(request))

@handle_errors
def org_industry_entity(request, entity_id, type):
    cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, type)

    if metadata['contributions']:
        amount = int(float(metadata['entity_info']['totals']['contributor_amount']))
        context['sections']['contributions'] = \
            org_contribution_section(entity_id, standardized_name, cycle, amount, type, metadata['entity_info']['external_ids'])

    if metadata['lobbying']:
        is_lobbying_firm = bool(metadata['entity_info']['metadata'].get('lobbying_firm', False))
        context['sections']['lobbying'] = \
            org_lobbying_section(entity_id, standardized_name, cycle, type, metadata['entity_info']['external_ids'], is_lobbying_firm)

    if 'regulations' in metadata and metadata['regulations']:
        context['sections']['regulations'] = \
            org_regulations_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'])

    if 'earmarks' in metadata and metadata['earmarks']:
        context['sections']['earmarks'] = \
            org_earmarks_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'])

    if metadata['fed_spending']:
        context['sections']['federal_spending'] = \
            org_spending_section(entity_id, standardized_name, cycle, metadata['entity_info']['totals'])

    if 'contractor_misconduct' in metadata and metadata['contractor_misconduct']:
        context['sections']['contractor_misconduct'] = \
            org_contractor_misconduct_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'])

    if 'epa_echo' in metadata and metadata['epa_echo']:
        context['sections']['epa_echo'] = \
            org_epa_echo_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'], metadata['entity_info']['totals'])

    if 'faca' in metadata and metadata['faca']:
        context['sections']['faca'] = org_faca_section(entity_id, standardized_name, cycle)

    return render_to_response('%s.html' % type, context,
                              entity_context(request, cycle, metadata['available_cycles']))

def org_contribution_section(entity_id, standardized_name, cycle, amount, type, external_ids):
    section = {
        'name': 'Campaign Finance',
        'template': 'contributions.html',
    }

    if type == 'industry':
        section['top_orgs'] = json.dumps([
            {
                'key': generate_label(str(OrganizationNameCleaver(org['name']).parse(safe=True))),
                'value': org['total_amount'],
                'value_employee': org['employee_amount'],
                'value_pac': org['direct_amount'],
                'href' : barchart_href(org, cycle, 'organization')
            } for org in api.org.industry_orgs(entity_id, cycle, limit=10)
        ])

    section['contributions_data'] = True
    recipients = api.org.recipients(entity_id, cycle=cycle)
    recipient_pacs = api.org.pac_recipients(entity_id, cycle)

    pol_recipients_barchart_data = []

    for record in recipients:
        if not record['name']:
            continue
        else:
            pol_recipients_barchart_data.append({
                    'key': generate_label(str(PoliticianNameCleaver(record['name']).parse().plus_metadata(record['party'], record['state']))),
                    'value' : record['total_amount'],
                    'value_employee' : record['employee_amount'],
                    'value_pac' : record['direct_amount'],
                    'href' : barchart_href(record, cycle, entity_type='politician')
                    })
    section['pol_recipients_barchart_data'] = json.dumps(bar_validate(pol_recipients_barchart_data))

    pacs_barchart_data = []
    for record in recipient_pacs:
        pacs_barchart_data.append({
                'key': generate_label(str(OrganizationNameCleaver(record['name']).parse(safe=True))),
                'value' : record['total_amount'],
                'value_employee' : record['employee_amount'],
                'value_pac' : record['direct_amount'],
                'href' : barchart_href(record, cycle, entity_type="organization"),
                })
    section['pacs_barchart_data'] = json.dumps(bar_validate(pacs_barchart_data))

    party_breakdown = api.org.party_breakdown(entity_id, cycle)
    for key, values in party_breakdown.iteritems():
        party_breakdown[key] = float(values[1])
    section['party_breakdown'] = json.dumps(pie_validate(party_breakdown))

    level_breakdown = api.org.level_breakdown(entity_id, cycle)
    for key, values in level_breakdown.iteritems():
        level_breakdown[key] = float(values[1])
    section['level_breakdown'] = json.dumps(pie_validate(level_breakdown))

    # if none of the charts have data, or if the aggregate total
    # received was negative, then suppress that whole content
    # section except the overview bar
    if amount <= 0:
        section['suppress_contrib_graphs'] = True
        if amount < 0:
            section['reason'] = "negative"

    elif (not section['pol_recipients_barchart_data']
          and not section['party_breakdown']
          and not section['level_breakdown']
          and not section['pacs_barchart_data']):
        section['suppress_contrib_graphs'] = True
        section['reason'] = 'empty'

    section['external_links'] = external_sites.get_contribution_links(type, standardized_name, external_ids, cycle)

    bundling = api.entities.bundles(entity_id, cycle)
    section['bundling_data'] = [ [x[key] for key in 'recipient_entity recipient_name recipient_type lobbyist_entity lobbyist_name firm_name amount'.split()] for x in bundling ]

    if int(cycle) == LATEST_CYCLE:
        section['fec_indexp'] = api.org.fec_indexp(entity_id)[:10]

        fec_summary = api.org.fec_summary(entity_id)
        if fec_summary and fec_summary['num_committee_filings'] > 0 and fec_summary.get('first_filing_date'):
            section['fec_summary'] = fec_summary
            section['fec_summary']['clean_date'] = datetime.datetime.strptime(section['fec_summary']['first_filing_date'], "%Y-%m-%d")
            top_contribs_data = [dict(key=generate_label(row['contributor_name'] if row['contributor_name'] else '<Name Missing>', 27),
                                        value=row['amount'], href='')
                                for row in api.org.fec_top_contribs(entity_id)
                                if float(row['amount']) >= 100000]
            if top_contribs_data:
                section['fec_top_contribs_data'] = json.dumps(top_contribs_data)

        if section.get('fec_indexp') or section.get('fec_summary'):
            section['include_fec'] = True

    return section


def org_lobbying_section(entity_id, name, cycle, type, external_ids, is_lobbying_firm):
    section = {
        'name': 'Lobbying',
        'template': '%s_lobbying.html' % ('org' if type == 'organization' else 'industry'),
    }

    section['lobbying_data'] = True
    section['is_lobbying_firm'] = is_lobbying_firm

    if is_lobbying_firm:
        section['lobbying_clients']   = api.org.registrant_clients(entity_id, cycle)
        section['lobbying_lobbyists'] = api.org.registrant_lobbyists(entity_id, cycle)
        section['lobbying_issues']    =  [item['issue'] for item in
                                       api.org.registrant_issues(entity_id, cycle)]
        section['lobbying_bills']     = [ {
            'bill': bill['bill_name'],
            'title': bill['title'],
            'link': make_bill_link(bill),
            'congress': bill['congress_no'],
        } for bill in api.org.registrant_bills(entity_id, cycle) ]
        section['lobbying_links'] = external_sites.get_lobbying_links('firm', name, external_ids, cycle)
    else:
        section['lobbying_clients']   = api.org.registrants(entity_id, cycle)
        section['lobbying_lobbyists'] = api.org.lobbyists(entity_id, cycle)
        section['lobbying_issues']    =  [item['issue'] for item in api.org.issues(entity_id, cycle)]
        section['lobbying_bills']     = [ {
            'bill': bill['bill_name'],
            'title': bill['title'],
            'link': make_bill_link(bill),
            'congress': bill['congress_no'],
        } for bill in api.org.bills(entity_id, cycle) ]

        section['lobbying_links'] = external_sites.get_lobbying_links('industry' if type == 'industry' else 'client', name, external_ids, cycle)

    section['lobbyist_registration_tracker'] = external_sites.get_lobbyist_tracker_data(external_ids)

    return section

def org_earmarks_section(entity_id, name, cycle, external_ids):
    section = {
        'name': 'Earmarks',
        'template': 'org_earmarks.html',
    }

    section['earmarks'] = earmarks_table_data(entity_id, cycle)
    section['earmark_links'] = external_sites.get_earmark_links('organization', name, external_ids, cycle)

    return section

def org_contractor_misconduct_section(entity_id, name, cycle, external_ids):
    section = {
        'name': 'Contractor Misconduct',
        'template': 'org_contractor_misconduct.html',
    }

    section['contractor_misconduct'] = api.org.contractor_misconduct(entity_id, cycle)
    section['pogo_links'] = external_sites.get_pogo_links(external_ids, name, cycle)

    return section


def org_epa_echo_section(entity_id, name, cycle, external_ids, totals):
    section = {
        'name': 'EPA Violations',
        'template': 'org_epa_echo.html',
    }

    section['epa_echo'] = api.org.epa_echo(entity_id, cycle)

    section['epa_found_things'] = totals['epa_actions_count']
    section['epa_links'] = external_sites.get_epa_links(name, cycle)

    return section


def org_spending_section(entity_id, name, cycle, totals):
    section = {
        'name': 'Federal Spending',
        'template': 'org_grants_and_contracts.html',
    }

    spending = api.org.fed_spending(entity_id, cycle)

    filter_bad_spending_descriptions(spending)

    section['grants_and_contracts'] = spending
    section['gc_links'] = external_sites.get_gc_links(name.__str__(), cycle)

    gc_found_things = []
    for gc_type in ['grant', 'contract', 'loan']:
        if totals.get('%s_count' % gc_type, 0):
            gc_found_things.append('%s %s%s' % (
                intcomma(totals['%s_count' % gc_type]),
                gc_type,
                pluralize(totals['%s_count' % gc_type])
            ))

    section['gc_found_things'] = gc_found_things

    return section

def org_regulations_section(entity_id, name, cycle, external_ids):
    section = {
        'name': 'Regulations',
        'template': 'org_regulations.html',
    }

    section['regulations_text'] = api.org.regulations_text(entity_id, cycle)
    section['regulations_submitter'] = api.org.regulations_submitter(entity_id, cycle)

    return section

def org_faca_section(entity_id, name, cycle):
    section = {
        'name': 'Advisory Committees',
        'template': 'org_faca.html',
    }

    section['faca'] = api.org.faca(entity_id, cycle=cycle)
    section['faca_links'] = external_sites.get_faca_links(name, cycle)

    return section

def organization_entity(request, entity_id):
    return org_industry_entity(request, entity_id, 'organization')


def industry_entity(request, entity_id):
    return org_industry_entity(request, entity_id, 'industry')


@handle_errors
def politician_entity(request, entity_id):
    cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, 'politician')

    if cycle == DEFAULT_CYCLE:
        """
            This section is to make sure we always display the most recently held seat,
            even if the candidate did not hold an office in the most recent cycle(s)
        """
        # get just the metadata that is the by cycle stuff
        cycle_info = [ (k,v) for k,v in metadata['entity_info']['metadata'].items() if k.isdigit() ]
        # this district_held check is a temporary hack
        # until we do a full contribution data reload
        sorted_cycles = sorted(cycle_info, key=lambda x: x[0] if x[1]['district_held'].strip() != '-' else 0)
        max_year_with_seat_held = sorted_cycles[-1][0]

        metadata['entity_info']['metadata']['seat_held']     = metadata['entity_info']['metadata'][max_year_with_seat_held]['seat_held']
        metadata['entity_info']['metadata']['district_held'] = metadata['entity_info']['metadata'][max_year_with_seat_held]['district_held']
        metadata['entity_info']['metadata']['state_held']    = metadata['entity_info']['metadata'][max_year_with_seat_held]['state_held']

    # make a shorter-named copy
    meta = metadata['entity_info']['metadata']
    # check that seat_held is properly defined and zero it out if not
    seat_held = meta['seat_held'] if meta['district_held'].strip() != '-' else ''
    metadata['entity_info']['metadata']['seat_held'] = seat_held

    metadata['entity_info']['name_with_meta'] = str(standardized_name.plus_metadata(meta.get('party'), meta.get('state')))

    if metadata['contributions']:
        amount = int(float(metadata['entity_info']['totals']['recipient_amount']))
        context['sections']['contributions'] = \
            pol_contribution_section(entity_id, standardized_name, cycle, amount, metadata['entity_info']['external_ids'])

    if metadata['earmarks']:
        context['sections']['earmarks'] = \
            pol_earmarks_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'])

    return render_to_response('politician.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))


def pol_contribution_section(entity_id, standardized_name, cycle, amount, external_ids):
    section = {
        'name': 'Campaign Finance',
        'template': 'contributions.html',
    }

    section['contributions_data'] = True

    top_contributors = api.pol.contributors(entity_id, cycle)
    top_industries = api.pol.industries(entity_id, cycle=cycle)

    section['pct_known'] = pct_contribs_from_known_industries(entity_id, cycle, amount)

    contributors_barchart_data = []
    for record in top_contributors:
        contributors_barchart_data.append({
            'key': generate_label(str(OrganizationNameCleaver(record['name']).parse(safe=True))),
            'value' : record['total_amount'],
            'value_employee' : record['employee_amount'],
            'value_pac' : record['direct_amount'],
            'href' : barchart_href(record, cycle, 'organization')
        })
    contributors_barchart_data = bar_validate(contributors_barchart_data)
    section['contributors_barchart_data'] = json.dumps(contributors_barchart_data)

    industries_barchart_data = []
    for record in top_industries:
        industries_barchart_data.append({
            'key': generate_label(str(OrganizationNameCleaver(record['name']).parse(safe=True))),
            'href': barchart_href(record, cycle, 'industry'),
            'value' : record['amount'],
        })
    industries_barchart_data = bar_validate(industries_barchart_data)
    section['industries_barchart_data'] = json.dumps(industries_barchart_data)

    local_breakdown = api.pol.local_breakdown(entity_id, cycle)
    for key, values in local_breakdown.iteritems():
        # values is a list of [count, amount]
        local_breakdown[key] = float(values[1])
    local_breakdown = pie_validate(local_breakdown)
    section['local_breakdown'] = json.dumps(local_breakdown)

    entity_breakdown = api.pol.contributor_type_breakdown(entity_id, cycle)
    for key, values in entity_breakdown.iteritems():
        # values is a list of [count, amount]
        entity_breakdown[key] = float(values[1])
    entity_breakdown = pie_validate(entity_breakdown)
    section['entity_breakdown'] = json.dumps(entity_breakdown)

    # if none of the charts have data, or if the aggregate total
    # received was negative, then suppress that whole content
    # section except the overview bar
    if amount < 0:
        section['suppress_contrib_graphs'] = True
        section['reason'] = "negative"

    elif not any((industries_barchart_data, contributors_barchart_data, local_breakdown, entity_breakdown)):
        section['suppress_contrib_graphs'] = True
        section['reason'] = 'empty'

    partytime_link, section['partytime_data'] = external_sites.get_partytime_data(external_ids)

    section['external_links'] = external_sites.get_contribution_links('politician', standardized_name.name_str(), external_ids, cycle)
    if partytime_link:
        section['external_links'].append({'url': partytime_link, 'text': 'Party Time'})

    bundling = api.entities.bundles(entity_id, cycle)
    section['bundling_data'] = [ [x[key] for key in 'lobbyist_entity lobbyist_name firm_entity firm_name amount'.split()] for x in bundling ]

    if int(cycle) == LATEST_CYCLE:
        section['fec_summary'] = api.pol.fec_summary(entity_id, cycle)
        if section['fec_summary']:
            section['include_fec'] = True

            if section['fec_summary'] and 'date' in section['fec_summary']:
                section['fec_summary']['clean_date'] = datetime.datetime.strptime(section['fec_summary']['date'], "%Y-%m-%d")

            timelines = []
            for pol in api.pol.fec_timeline(entity_id, cycle):
                tl = {
                    'name': pol['candidate_name'],
                    'party': pol['party'],
                    'is_this': pol['entity_id'] == entity_id,
                    'timeline': map(lambda item: item if item >= 0 else 0, pol['timeline']),
                    'href': '/politician/%s/%s?cycle=%s' % (slugify(PoliticianNameCleaver(pol['candidate_name']).parse().name_str()), pol['entity_id'], cycle)
                }
                tl['sum'] = sum(tl['timeline'])
                timelines.append(tl)
            timelines.sort(key=lambda t: (int(t['is_this']), t['sum']), reverse=True)
            # restrict to top 5, and only those receiving at least 10% of this pol's total
            if timelines:
                this_sum = timelines[0]['sum']
                timelines = [timeline for timeline in timelines if timeline['sum'] > 0.1 * this_sum]
                timelines = timelines[:5]

            section['fec_timelines'] = json.dumps(timelines)

            section['fec_indexp'] = api.pol.fec_indexp(entity_id, cycle)[:10]

    return section


def pct_contribs_from_known_industries(entity_id, cycle, amount):
    industries_unknown_amount = api.pol.industries_unknown(entity_id, cycle=cycle).get('amount', 0)

    pct_unknown = 0

    if amount:
        pct_unknown = float(industries_unknown_amount) * 100 / amount

    return int(round(100 - pct_unknown))


def earmarks_table_data(entity_id, cycle):
    rows = api.pol.earmarks(entity_id, cycle)
    for row in rows:
        for member in row['members']:
            member['name'] = str(PoliticianNameCleaver(member['name']).parse().plus_metadata(member['party'], member['state']))

    return rows


def pol_earmarks_section(entity_id, name, cycle, external_ids):
    section = {
        'name': 'Earmarks',
        'template': 'pol_earmarks.html',
    }

    section['earmarks'] = earmarks_table_data(entity_id, cycle)

    local_breakdown = api.pol.earmarks_local_breakdown(entity_id, cycle)
    local_breakdown = dict([(key, float(value[1])) for key, value in local_breakdown.iteritems()])

    section['earmark_links'] = external_sites.get_earmark_links('politician', name.name_str(), external_ids, cycle)

    ordered_pie = SortedDict([(key, local_breakdown.get(key, 0)) for key in ['unknown', 'in-state', 'out-of-state']])
    section['earmarks_local'] = json.dumps(pie_validate(ordered_pie))

    return section


@handle_errors
def individual_entity(request, entity_id):
    cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, 'individual')

    if metadata['contributions']:
        amount = int(float(metadata['entity_info']['totals']['contributor_amount']))
        context['sections']['contributions'] = \
            indiv_contribution_section(entity_id, standardized_name, cycle, amount, metadata['entity_info']['external_ids'])

    if metadata['lobbying']:
        context['sections']['lobbying'] = \
            indiv_lobbying_section(entity_id, standardized_name, cycle, metadata['entity_info']['external_ids'])

    return render_to_response('individual.html', context,
                              entity_context(request, cycle, metadata['available_cycles']))


def indiv_contribution_section(entity_id, standardized_name, cycle, amount, external_ids):
    section = {
        'name': 'Campaign Finance',
        'template': 'contributions.html',
    }

    section['contributions_data'] = True
    recipient_candidates = api.indiv.pol_recipients(entity_id, cycle)
    recipient_orgs = api.indiv.org_recipients(entity_id, cycle)

    candidates_barchart_data = []
    for record in recipient_candidates:
        candidates_barchart_data.append({
                'key': generate_label(str(PoliticianNameCleaver(record['recipient_name']).parse().plus_metadata(record['party'], record['state']))),
                'value' : record['amount'],
                'href' : barchart_href(record, cycle, entity_type="politician"),
                })
    section['candidates_barchart_data'] = json.dumps(bar_validate(candidates_barchart_data))

    orgs_barchart_data = []
    for record in recipient_orgs:
        orgs_barchart_data.append({
                'key': generate_label(str(OrganizationNameCleaver(record['recipient_name']).parse(safe=True))),
                'value' : record['amount'],
                'href' : barchart_href(record, cycle, entity_type="organization"),
                })
    section['orgs_barchart_data'] = json.dumps(bar_validate(orgs_barchart_data))

    party_breakdown = api.indiv.party_breakdown(entity_id, cycle)
    for key, values in party_breakdown.iteritems():
        party_breakdown[key] = float(values[1])
    section['party_breakdown'] = json.dumps(pie_validate(party_breakdown))

    # if none of the charts have data, or if the aggregate total
    # received was negative, then suppress that whole content
    # section except the overview bar
    if amount < 0:
        section['suppress_contrib_graphs'] = True
        section['reason'] = "negative"

    elif (not section['candidates_barchart_data']
        and not section['orgs_barchart_data']
        and not section['party_breakdown']):
        section['suppress_contrib_graphs'] = True
        section['reason'] = 'empty'

    section['external_links'] = external_sites.get_contribution_links('individual', standardized_name, external_ids, cycle)

    bundling = api.entities.bundles(entity_id, cycle)
    section['bundling_data'] = [ [x[key] for key in 'recipient_entity recipient_name recipient_type firm_entity firm_name amount'.split()] for x in bundling ]

    return section


def indiv_lobbying_section(entity_id, name, cycle, external_ids):
    section = {
        'name': 'Lobbying',
        'template': 'indiv_lobbying.html',
    }

    section['lobbying_data'] = True
    section['lobbying_with_firm'] = api.indiv.registrants(entity_id, cycle)
    section['issues_lobbied_for'] =  [item['issue'] for item in api.indiv.issues(entity_id, cycle)]
    section['lobbying_for_clients'] = api.indiv.clients(entity_id, cycle)
    section['lobbying_links'] = external_sites.get_lobbying_links('lobbyist', name, external_ids, cycle)

    return section


