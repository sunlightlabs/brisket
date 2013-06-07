# coding=utf-8

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import pluralize, slugify
from django.utils.datastructures import SortedDict
from feedinator.models import Feed
from influence import external_sites
from influence.helpers import generate_label, barchart_href, \
    bar_validate, pie_validate, earmarks_table_data, \
    filter_bad_spending_descriptions, make_bill_link, get_top_pages
from influenceexplorer import DEFAULT_CYCLE
from influence.external_sites import _get_td_url
from influence.base_views import EntityView, Section
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver
from name_cleaver.names import PoliticianName
from settings import LATEST_CYCLE, TOP_LISTS_CYCLE, DOCKETWRENCH_URL, api
from urllib2 import URLError, HTTPError
import datetime
import json
import unicodedata


# Exceptions need a functioning unicode method
# for Sentry. URLError and its subclass HTTPError
# do not. So monkey patching.
URLError.__unicode__ = lambda self: unicode(self.__str__())

def entity_redirect(request, entity_id):
    entity = api.entities.metadata(entity_id)

    name = slugify(entity['name'])

    return redirect('{}_entity'.format(entity['type']), entity_id=entity_id)

### Organizations and Industries ###

class OrgContributionSection(Section):
    name = 'Campaign Finance'
    template = 'entities/contributions.html'
    label = 'contributions'
    
    def should_fetch(self):
        return bool(self.entity.metadata['contributions'])

    def fetch(self):
        entity_id, cycle = self.entity.entity_id, self.entity.cycle

        if self.entity.type == 'industry':
            self.data['industry_orgs'] = api.org.industry_orgs(entity_id, cycle, limit=10)
        self.data['recipients'] = api.org.recipients(entity_id, cycle=cycle)
        self.data['recipient_pacs'] = api.org.pac_recipients(entity_id, cycle)
        self.data['party_breakdown'] = api.org.party_breakdown(entity_id, cycle)
        self.data['level_breakdown'] = api.org.level_breakdown(entity_id, cycle)
        self.data['bundling'] = api.entities.bundles(entity_id, cycle)
        if int(cycle) != -1:
            self.data['fec_indexp'] = api.org.fec_indexp(entity_id, cycle)[:10]
            self.data['fec_summary'] = api.org.fec_summary(entity_id, cycle)
            self.data['fec_top_contribs'] = api.org.fec_top_contribs(entity_id, cycle)
        return True

    def build_section_data(self):
        entity_id, cycle, type, standardized_name, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.type, self.entity.standardized_name, self.entity.external_ids
        amount = int(float(self.entity.metadata['entity_info']['totals']['contributor_amount']))

        if type == 'industry':
            self.top_orgs = json.dumps([
                {
                    'key': generate_label(str(OrganizationNameCleaver(org['name']).parse())),
                    'value': org['total_amount'],
                    'value_employee': org['employee_amount'],
                    'value_pac': org['direct_amount'],
                    'href' : barchart_href(org, cycle, 'organization')
                } for org in self.data['industry_orgs']
            ])

        self.contributions_data = True

        pol_recipients_barchart_data = []
        for record in self.data['recipients']:
            pol_recipients_barchart_data.append({
                'key': generate_label(str(PoliticianNameCleaver(record['name']).parse().plus_metadata(record['party'], record['state']))),
                'value' : record['total_amount'],
                'value_employee' : record['employee_amount'],
                'value_pac' : record['direct_amount'],
                'href' : barchart_href(record, cycle, entity_type='politician')
            })
        self.pol_recipients_barchart_data = json.dumps(bar_validate(pol_recipients_barchart_data))

        pacs_barchart_data = []
        for record in self.data['recipient_pacs']:
            pacs_barchart_data.append({
                'key': generate_label(str(OrganizationNameCleaver(record['name']).parse())),
                'value' : record['total_amount'],
                'value_employee' : record['employee_amount'],
                'value_pac' : record['direct_amount'],
                'href' : barchart_href(record, cycle, entity_type="organization"),
            })
        self.pacs_barchart_data = json.dumps(bar_validate(pacs_barchart_data))

        for key, values in self.data['party_breakdown'].iteritems():
            self.data['party_breakdown'][key] = float(values[1])
        self.party_breakdown = json.dumps(pie_validate(self.data['party_breakdown']))

        for key, values in self.data['level_breakdown'].iteritems():
            self.data['level_breakdown'][key] = float(values[1])
        self.level_breakdown = json.dumps(pie_validate(self.data['level_breakdown']))

        # if none of the charts have data, or if the aggregate total
        # received was negative, then suppress that whole content
        # section except the overview bar
        if amount <= 0:
            self.suppress_contrib_graphs = True
            if amount < 0:
                self.reason = "negative"

        elif (not self.pol_recipients_barchart_data
              and not self.party_breakdown
              and not self.level_breakdown
              and not self.pacs_barchart_data):
            self.suppress_contrib_graphs = True
            self.reason = 'empty'

        self.external_links = external_sites.get_contribution_links(type, standardized_name, external_ids, cycle)

        self.bundling_data = [[x[key] for key in 'recipient_entity recipient_name recipient_type lobbyist_entity lobbyist_name firm_name amount'.split()] for x in self.data['bundling']]

        if int(cycle) != -1:
            self.fec_indexp = self.data['fec_indexp']

            if self.data['fec_summary'] and self.data['fec_summary']['num_committee_filings'] > 0 and self.data['fec_summary'].get('first_filing_date'):
                self.fec_summary = self.data['fec_summary']
                self.fec_summary['clean_date'] = datetime.datetime.strptime(self.fec_summary['first_filing_date'], "%Y-%m-%d")
                top_contribs_data = [dict(key=generate_label(row['contributor_name'] if row['contributor_name'] else '<Name Missing>', 27),
                                            value=row['amount'], href='')
                                    for row in self.data['fec_top_contribs']
                                    if float(row['amount']) >= 100000]
                if top_contribs_data:
                    self.fec_top_contribs_data = json.dumps(top_contribs_data)

            if getattr(self, 'fec_indexp', False) or getattr(self, 'fec_summary', False):
                self.include_fec = True


class OrgLobbyingSection(Section):
    name = 'Lobbying'
    label = 'lobbying'

    @property
    def template(self):
        return 'entities/%s_lobbying.html' % ('org' if self.entity.type == 'organization' else 'industry')

    
    def should_fetch(self):
        return bool(self.entity.metadata['lobbying'])

    def fetch(self):
        entity_id, cycle, type, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.type, self.entity.external_ids

        self.entity_is_lobbying_firm = bool(self.entity.metadata['entity_info']['metadata'].get('lobbying_firm', False))
        if self.entity_is_lobbying_firm:
            self.lobbying_clients   = api.org.registrant_clients(entity_id, cycle)
            self.lobbying_lobbyists = api.org.registrant_lobbyists(entity_id, cycle)
            self.data['lobbying_issues'] = api.org.registrant_issues(entity_id, cycle)
            self.data['lobbying_bills'] = api.org.registrant_bills(entity_id, cycle)
        else:
            self.lobbying_clients   = api.org.registrants(entity_id, cycle)
            self.lobbying_lobbyists = api.org.lobbyists(entity_id, cycle)
            self.data['lobbying_issues'] = api.org.issues(entity_id, cycle)
            self.data['lobbying_bills'] = api.org.bills(entity_id, cycle)
        self.lobbyist_registration_tracker = external_sites.get_lobbyist_tracker_data(external_ids)

        return True

    def build_section_data(self):
        entity_id, name, cycle, type, external_ids, is_lobbying_firm = \
            self.entity.entity_id, self.entity.standardized_name, self.entity.cycle, self.entity.type, self.entity.external_ids, self.entity_is_lobbying_firm

        self.lobbying_data = True
        self.is_lobbying_firm = is_lobbying_firm

        if is_lobbying_firm:
            self.lobbying_issues    =  [item['issue'] for item in self.data['lobbying_issues']]
            self.lobbying_bills     = [{
                'bill': bill['bill_name'],
                'title': bill['title'],
                'link': make_bill_link(bill),
                'congress': bill['congress_no'],
            } for bill in self.data['lobbying_bills']]
            self.lobbying_links = external_sites.get_lobbying_links('firm', name, external_ids, cycle)
        else:
            self.lobbying_issues    =  [item['issue'] for item in self.data['lobbying_issues']]
            self.lobbying_bills     = [ {
                'bill': bill['bill_name'],
                'title': bill['title'],
                'link': make_bill_link(bill),
                'congress': bill['congress_no'],
            } for bill in self.data['lobbying_bills']]
            self.lobbying_links = external_sites.get_lobbying_links('industry' if type == 'industry' else 'client', name, external_ids, cycle)

class OrgEarmarksSection(Section):
    name = 'Earmarks'
    template = 'entities/org_earmarks.html'
    label = 'earmarks'
    
    def should_fetch(self):
        return 'earmarks' in self.entity.metadata and self.entity.metadata['earmarks']

    def fetch(self):
        self.earmarks = earmarks_table_data(self.entity.entity_id, self.entity.cycle)
        return True
    
    def build_section_data(self):
        self.earmark_links = external_sites.get_earmark_links('organization', self.entity.standardized_name, self.entity.external_ids, self.entity.cycle)

class OrgContractorMisconductSection(Section):
    name = 'Contractor Misconduct'
    template = 'entities/org_contractor_misconduct.html'
    label = 'contractor_misconduct'

    def should_fetch(self):
        return 'contractor_misconduct' in self.entity.metadata and self.entity.metadata['contractor_misconduct']

    def fetch(self):
        self.contractor_misconduct = api.org.contractor_misconduct(self.entity.entity_id, self.entity.cycle)
        return True

    def build_section_data(self):
        self.pogo_links = external_sites.get_pogo_links(self.entity.external_ids, self.entity.standardized_name, self.entity.cycle)

class OrgEpaEchoSection(Section):
    name = 'EPA Violations'
    template = 'entities/org_epa_echo.html'
    label = 'epa_echo'
    
    def should_fetch(self):
        return 'epa_echo' in self.entity.metadata and self.entity.metadata['epa_echo']

    def fetch(self):
        self.epa_echo = api.org.epa_echo(self.entity.entity_id, self.entity.cycle)
        return True

    def build_section_data(self):
        self.epa_found_things = self.entity.metadata['entity_info']['totals']['epa_actions_count']
        self.epa_links = external_sites.get_epa_links(self.entity.standardized_name, self.entity.cycle)

class OrgSpendingSection(Section):
    name = 'Federal Spending'
    template = 'entities/org_grants_and_contracts.html'
    label = 'federal_spending'
    
    def should_fetch(self):
        return bool(self.entity.metadata['fed_spending'])

    def fetch(self):
        self.data['spending'] = api.org.fed_spending(self.entity.entity_id, self.entity.cycle)
        return True

    def build_section_data(self):
        cycle, name, totals = self.entity.cycle, self.entity.standardized_name, self.entity.metadata['entity_info']['totals']

        filter_bad_spending_descriptions(self.data['spending'])

        self.grants_and_contracts = self.data['spending']
        self.gc_links = external_sites.get_gc_links(name.__str__(), cycle)

        gc_found_things = []
        for gc_type in ['grant', 'contract', 'loan']:
            if totals.get('%s_count' % gc_type, 0):
                gc_found_things.append('%s %s%s' % (
                    intcomma(totals['%s_count' % gc_type]),
                    gc_type,
                    pluralize(totals['%s_count' % gc_type])
                ))

        self.gc_found_things = gc_found_things

class OrgRegulationsSection(Section):
    name = 'Regulations'
    template = 'entities/org_regulations.html'
    label = 'regulations'

    def fetch(self):
        try:
            self.data['dw_data'] = external_sites.get_docketwrench_entity_data(self.entity.entity_id, self.entity.cycle)
        except HTTPError as e:
            if e.code == 404:
                return False
            else:
                raise
        return True

    def build_section_data(self):
        dw_data = self.data['dw_data']
        try:
            self.regulations_text = dw_data['stats']['text_mentions']['top_dockets']
            self.regulations_submitter = dw_data['stats']['submitter_mentions']['top_dockets']
        except KeyError:
            self.enabled = False
            return

        rdg_generic = {
            'url': 'http://regulations.gov',
            'text': 'Regulations.gov'
        }
        self.regulations_text_links = [{
            'url': "http://docketwrench.sunlightfoundation.com" + dw_data['stats']['text_mentions']['docket_search_url'],
            'text': "mentions"
        }, rdg_generic]
        self.regulations_submitter_links = [{
            'url': "http://docketwrench.sunlightfoundation.com" + dw_data['stats']['submitter_mentions']['docket_search_url'],
            'text': "submissions"
        }, rdg_generic]

        self.regulations_text_count = dw_data['stats']['text_mentions']['docket_count']
        self.regulations_submitter_count = dw_data['stats']['submitter_mentions']['docket_count']
    
class OrgFacaSection(Section):
    name = 'Advisory Committees'
    template = 'entities/org_faca.html'
    label = 'faca'

    def should_fetch(self):
        return 'faca' in self.entity.metadata and self.entity.metadata['faca']

    def fetch(self):
        self.faca = api.org.faca(self.entity.entity_id, cycle=self.entity.cycle)
        return True

    def build_section_data(self):
        self.faca_links = external_sites.get_faca_links(self.entity.standardized_name, self.entity.cycle)

class OrganizationEntityView(EntityView):
    type = 'organization'
    sections = [
        OrgContributionSection,
        OrgLobbyingSection,
        OrgRegulationsSection,
        OrgEarmarksSection,
        OrgSpendingSection,
        OrgContractorMisconductSection,
        OrgEpaEchoSection,
        OrgFacaSection
    ]

class IndustryEntityView(EntityView):
    type = 'industry'
    sections = [
        OrgContributionSection,
        OrgLobbyingSection
    ]


### Politicians ###

class PolContributionSection(Section):
    name = 'Campaign Finance'
    template = 'entities/contributions.html'
    label = 'contributions'

    def should_fetch(self):
        return bool(self.entity.metadata['contributions'])
    
    def fetch(self):
        entity_id, cycle, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.external_ids
        self.data['top_contributors'] = api.pol.contributors(entity_id, cycle)
        self.data['top_industries'] = api.pol.industries(entity_id, cycle=cycle)
        self.data['industries_unknown_amount'] = api.pol.industries_unknown(entity_id, cycle=cycle)
        self.data['local_breakdown'] = api.pol.local_breakdown(entity_id, cycle)
        self.data['entity_breakdown'] = api.pol.contributor_type_breakdown(entity_id, cycle)
        self.partytime_link, self.partytime_data = external_sites.get_partytime_data(external_ids)
        self.data['bundling'] = api.entities.bundles(entity_id, cycle)
        self.fec_summary = api.pol.fec_summary(entity_id, cycle) if int(cycle) != -1 else None
        if self.fec_summary:
            self.data['fec_timeline'] = api.pol.fec_timeline(entity_id, cycle)
            self.fec_indexp = api.pol.fec_indexp(entity_id, cycle)[:10]

        return True

    def build_section_data(self):
        entity_id, standardized_name, cycle, external_ids = self.entity.entity_id, self.entity.standardized_name, self.entity.cycle, self.entity.external_ids

        self.contributions_data = True

        contributors_barchart_data = []
        for record in self.data['top_contributors']:
            contributors_barchart_data.append({
                'key': generate_label(str(OrganizationNameCleaver(record['name']).parse())),
                'value' : record['total_amount'],
                'value_employee' : record['employee_amount'],
                'value_pac' : record['direct_amount'],
                'href' : barchart_href(record, cycle, 'organization')
            })
        contributors_barchart_data = bar_validate(contributors_barchart_data)
        self.contributors_barchart_data = json.dumps(contributors_barchart_data)

        industries_barchart_data = []
        for record in self.data['top_industries']:
            industries_barchart_data.append({
                'key': generate_label(str(OrganizationNameCleaver(record['name']).parse())),
                'href': barchart_href(record, cycle, 'industry'),
                'value' : record['amount'],
            })
        industries_barchart_data = bar_validate(industries_barchart_data)
        self.industries_barchart_data = json.dumps(industries_barchart_data)

        for key, values in self.data['local_breakdown'].iteritems():
            # values is a list of [count, amount]
            self.data['local_breakdown'][key] = float(values[1])
        self.data['local_breakdown'] = pie_validate(self.data['local_breakdown'])
        self.local_breakdown = json.dumps(self.data['local_breakdown'])

        for key, values in self.data['entity_breakdown'].iteritems():
            # values is a list of [count, amount]
            self.data['entity_breakdown'][key] = float(values[1])
        self.data['entity_breakdown'] = pie_validate(self.data['entity_breakdown'])
        self.entity_breakdown = json.dumps(self.data['entity_breakdown'])

        # if none of the charts have data, or if the aggregate total
        # received was negative, then suppress that whole content
        # section except the overview bar
        amount = int(float(self.entity.metadata['entity_info']['totals']['recipient_amount']))
        if amount < 0:
            self.suppress_contrib_graphs = True
            self.reason = "negative"
        elif not any((industries_barchart_data, contributors_barchart_data, self.data['local_breakdown'], self.data['entity_breakdown'])):
            self.suppress_contrib_graphs = True
            self.reason = 'empty'

        pct_unknown = 0
        if amount:
            pct_unknown = float(self.data['industries_unknown_amount'].get('amount', 0)) * 100 / amount
        self.pct_known = int(round(100 - pct_unknown))
        
        self.external_links = external_sites.get_contribution_links('politician', standardized_name.name_str(), external_ids, cycle)
        if self.partytime_link:
            self.external_links.append({'url': self.partytime_link, 'text': 'Party Time'})
        
        self.bundling_data = [[x[key] for key in 'lobbyist_entity lobbyist_name firm_entity firm_name amount'.split()] for x in self.data['bundling']]

        if self.fec_summary:
            self.include_fec = True

            if self.fec_summary and 'date' in self.fec_summary:
                self.fec_summary['clean_date'] = datetime.datetime.strptime(self.fec_summary['date'], "%Y-%m-%d")
        
            timelines = []
            for pol in self.data['fec_timeline']:
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
        
            self.fec_timelines = json.dumps(timelines)

class PolEarmarksSection(Section):
    name = 'Earmarks'
    template = 'entities/pol_earmarks.html'
    label = 'earmarks'

    def should_fetch(self):
        return bool(self.entity.metadata['earmarks'])
    
    def fetch(self):
        entity_id, cycle, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.external_ids

        self.earmarks = earmarks_table_data(entity_id, cycle)
        self.data['local_breakdown'] = api.pol.earmarks_local_breakdown(entity_id, cycle)
        return True

    def build_section_data(self):
        entity_id, cycle, standardized_name, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.standardized_name, self.entity.external_ids

        local_breakdown = dict([(key, float(value[1])) for key, value in self.data['local_breakdown'].iteritems()])

        self.earmark_links = external_sites.get_earmark_links('politician', standardized_name.name_str(), external_ids, cycle)

        ordered_pie = SortedDict([(key, local_breakdown.get(key, 0)) for key in
            ['Unknown', 'In-State', 'Out-of-State']])
        self.earmarks_local = json.dumps(pie_validate(ordered_pie))


class PoliticianEntityView(EntityView):
    type = 'politician'
    sections = [
        PolContributionSection,
        PolEarmarksSection
    ]

    def prepare_context(self, request):
        context = super(PoliticianEntityView, self).prepare_context(request)

        metadata, cycle = self.metadata, self.cycle
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
        seat_held = meta.get('seat_held') if meta.get('district_held', '').strip() != '-' else ''
        metadata['entity_info']['metadata']['seat_held'] = seat_held

        metadata['entity_info']['name_with_meta'] = str(self.standardized_name.plus_metadata(meta.get('party'), meta.get('state')))

        return context


### Individuals ###

class IndivContributionSection(Section):
    name = 'Campaign Finance'
    template = 'entities/contributions.html'
    label = 'contributions'
    
    def should_fetch(self):
        return bool(self.entity.metadata['contributions'])

    def fetch(self):
        entity_id, cycle, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.external_ids
        self.data['recipient_candidates'] = api.indiv.pol_recipients(entity_id, cycle)
        self.data['recipient_orgs'] = api.indiv.org_recipients(entity_id, cycle)
        self.data['party_breakdown'] = api.indiv.party_breakdown(entity_id, cycle)
        self.data['bundling'] = api.entities.bundles(entity_id, cycle)
        return True
    
    def build_section_data(self):
        entity_id, cycle, standardized_name, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.standardized_name, self.entity.external_ids
        self.contributions_data = True

        candidates_barchart_data = []
        for record in self.data['recipient_candidates']:
            candidates_barchart_data.append({
                'key': generate_label(str(PoliticianNameCleaver(record['recipient_name']).parse().plus_metadata(record['party'], record['state']))),
                'value' : record['amount'],
                'href' : barchart_href(record, cycle, entity_type="politician"),
            })
        self.candidates_barchart_data = json.dumps(bar_validate(candidates_barchart_data))

        orgs_barchart_data = []
        for record in self.data['recipient_orgs']:
            orgs_barchart_data.append({
                'key': generate_label(str(OrganizationNameCleaver(record['recipient_name']).parse())),
                'value' : record['amount'],
                'href' : barchart_href(record, cycle, entity_type="organization"),
            })
        self.orgs_barchart_data = json.dumps(bar_validate(orgs_barchart_data))

        for key, values in self.data['party_breakdown'].iteritems():
            self.data['party_breakdown'][key] = float(values[1])
        self.party_breakdown = json.dumps(pie_validate(self.data['party_breakdown']))

        # if none of the charts have data, or if the aggregate total
        # received was negative, then suppress that whole content
        # section except the overview bar
        amount = int(float(self.entity.metadata['entity_info']['totals']['contributor_amount']))
        if amount < 0:
            self.suppress_contrib_graphs = True
            self.reason = "negative"

        elif (not self.candidates_barchart_data
            and not self.orgs_barchart_data
            and not self.party_breakdown):
            self.suppress_contrib_graphs = True
            self.reason = 'empty'

        self.external_links = external_sites.get_contribution_links('individual', standardized_name, external_ids, cycle)

        self.bundling_data = [[x[key] for key in 'recipient_entity recipient_name recipient_type firm_entity firm_name amount'.split()] for x in self.data['bundling']]


class IndivLobbyingSection(Section):
    name = 'Lobbying'
    template = 'entities/indiv_lobbying.html'
    label = 'lobbying'
    
    def should_fetch(self):
        return bool(self.entity.metadata['lobbying'])

    def fetch(self):
        entity_id, cycle, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.external_ids
        self.lobbying_with_firm = api.indiv.registrants(entity_id, cycle)
        self.data['issues'] = api.indiv.issues(entity_id, cycle)
        self.lobbying_for_clients = api.indiv.clients(entity_id, cycle)
        return True

    def build_section_data(self):
        entity_id, cycle, standardized_name, external_ids = self.entity.entity_id, self.entity.cycle, self.entity.standardized_name, self.entity.external_ids
        self.lobbying_data = True
        self.issues_lobbied_for =  [item['issue'] for item in self.data['issues']]
        self.lobbying_links = external_sites.get_lobbying_links('lobbyist', standardized_name, external_ids, cycle)

class IndividualEntityView(EntityView):
    type = 'individual'
    sections = [
        IndivContributionSection,
        IndivLobbyingSection
    ]

# map all the entity view classes for later use
entity_views = {}
for klass in globals().values():
    if type(klass) == type and issubclass(klass, EntityView) and klass.type:
        entity_views[klass.type] = klass

### Preview Views ###
class PoliticianPreviewView(PoliticianEntityView):
    sections = []
    template = "entities/politician_preview.html"

def entity_preview_redirect(request, entity_id, type=None):
    entity = api.entities.metadata(entity_id)
    if entity['type'] == 'politician':
        name = slugify(entity['name'])
        return redirect('{}_preview'.format(entity['type']), entity_id=entity_id)
    else:
        return redirect('{}_entity'.format(entity['type']), entity_id=entity_id)
