# coding=utf-8

import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from settings import TOP_LISTS_CYCLE, api
from influence.base_views import EntityLandingView, Section, \
                                 EntityLandingSection

### Groups ###
class IndustryContributionsLandingSection(Section):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/industry_landing_contributions.html'
    enabled = False

class IndustryLobbyingLandingSection(Section):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/industry_landing_lobbying.html'
    enabled = False

class IndustryGrantsAndContractsLandingSection(Section):
    name = 'Federal Spending'
    label = 'grants_and_contracts'
    template = 'entity_landing/industry_landing_grants_and_contracts.html'
    enabled = False

class IndustryLandingView(EntityLandingView):
    label = 'industry'
    name = 'Industries'
    sections = [
        IndustryContributionsLandingSection,
        IndustryLobbyingLandingSection,
        IndustryGrantsAndContractsLandingSection,
    ]

class OrgContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/org_landing_contributions.html'

    #def should_fetch(self):
    #    return bool(self.entity.summaries[self.label])

    #def fetch(self):
    #    self.data = self.entity.summaries[self.label]
    #    return True

    def build_section_data(self):
        self.total_contribution_amount = sum([float(n['amount']) for n in self.data['state_fed_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.pac_indiv_summary_data = self.prepare_parent_child_tree('pac_indiv_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')
        self.seat_summary_data = self.prepare_parent_child_tree('seat_summary')

        if self.total_contribution_amount <= 0:
            self.suppress_contrib_graphs = True
            if self.total_contribution_amount < 0:
                self.reason = "negative"

class OrgLobbyingLandingSection(EntityLandingSection):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/org_landing_lobbying.html'
    enabled = False
    
    def build_section_data(self):
        self.bills_summary_data = self.prepare_parent_child_tree('bills_summary')
        self.issues_summary_data = self.prepare_parent_child_tree('issues_summary')

        # TODO: add metadata
        # http://congress.api.sunlightfoundation.com/bills?bill_type={bill_type}&number={bill_number}&congress={congress_number}&apikey=sunlight9&fields=official_title,short_title,title,popular_title,nicknames,last_action,summary_short

class OrgRegulationsLandingSection(EntityLandingSection):
    name = 'Regulations'
    label = 'regulations'
    template = 'entity_landing/org_landing_regulations.html'
    enabled = False

class OrgEarmarksLandingSection(EntityLandingSection):
    name = 'Earmarks'
    label = 'earmarks'
    template = 'entity_landing/org_landing_earmarks.html'
    enabled = False

class OrgGrantsAndContractsLandingSection(EntityLandingSection):
    name = 'Federal Spending'
    label = 'grants_and_contracts'
    template = 'entity_landing/org_landing_grants_and_contracts.html'
    enabled = False

class OrgContractorMisconductLandingSection(EntityLandingSection):
    name = 'Contractor Misconduct'
    label = 'contractor_misconduct'
    template = 'entity_landing/org_landing_contractor_misconduct.html'
    enabled = False

class OrgEpaEchoLandingSection(EntityLandingSection):
    name = 'EPA Violations'
    label = 'epa_echo'
    template = 'entity_landing/org_landing_epa_echo.html'
    enabled = False

class OrgFacaLandingSection(EntityLandingSection):
    name = 'Advisory Committees'
    label = 'faca'
    template = 'entity_landing/org_landing_faca.html'
    enabled = False

class OrgLandingView(EntityLandingView):
    label = 'org'
    name = 'Organizations'
    sections = [
        OrgContributionsLandingSection,
        OrgLobbyingLandingSection,
        OrgRegulationsLandingSection,
        OrgEarmarksLandingSection,
        OrgGrantsAndContractsLandingSection,
        OrgContractorMisconductLandingSection,
        OrgEpaEchoLandingSection,
        OrgFacaLandingSection,
    ]

class PolGroupContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/pol_group_landing_contributions.html'
    enabled = True

    def build_section_data(self):
        self.total_contribution_amount = sum([float(n['amount']) for n in self.data['state_fed_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.pac_indiv_summary_data = self.prepare_parent_child_tree('pac_indiv_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')
        self.seat_summary_data = self.prepare_parent_child_tree('seat_summary')

        if self.total_contribution_amount <= 0:
            self.suppress_contrib_graphs = True
            if self.total_contribution_amount < 0:
                self.reason = "negative"

class PolGroupLobbyingLandingSection(EntityLandingSection):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/pol_group_landing_lobbying.html'
    enabled = False

class PolGroupRegulationsLandingSection(EntityLandingSection):
    name = 'Regulations'
    label = 'regulations'
    template = 'entity_landing/pol_group_landing_regulations.html'
    enabled = False

class PolGroupFacaLandingSection(EntityLandingSection):
    name = 'Advisory Committees'
    label = 'faca'
    template = 'entity_landing/pol_group_landing_faca.html'
    enabled = False

class PolGroupLandingView(EntityLandingView):
    label = 'pol_group'
    name = 'Political Groups'
    sections = [
        PolGroupContributionsLandingSection,
    ]

class LobbyingOrgContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/lobbying_org_landing_contributions.html'
    enabled = False

class LobbyingOrgLobbyingLandingSection(EntityLandingSection):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/lobbying_org_landing_lobbying.html'
    enabled = False

class LobbyingOrgRegulationsLandingSection(EntityLandingSection):
    name = 'Regulations'
    label = 'regulations'
    template = 'entity_landing/lobbying_org_landing_regulations.html'
    enabled = False

class LobbyingOrgFacaLandingSection(EntityLandingSection):
    name = 'Advisory Committees'
    label = 'faca'
    template = 'entity_landing/lobbying_org_landing_faca.html'
    enabled = False

class LobbyingOrgLandingView(EntityLandingView):
    label = 'lobbying_org'
    name = 'Lobbying Firms'
    sections = [
        LobbyingOrgContributionsLandingSection,
        LobbyingOrgLobbyingLandingSection,
        LobbyingOrgRegulationsLandingSection,
        LobbyingOrgFacaLandingSection,
    ]

### People ###
class IndividualContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/individual_landing_contributions.html'
    enabled = True

    def build_section_data(self):
        self.total_contribution_amount = sum([float(n['amount']) for n in self.data['state_fed_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.recipient_type_summary_data = self.prepare_parent_child_tree('recipient_type_summary')
        self.seat_summary_data = self.prepare_parent_child_tree('seat_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')
        self.in_state_out_of_state_summary_data = self.prepare_parent_child_tree('in_state_out_of_state_summary')
        
        if self.total_contribution_amount <= 0:
            self.suppress_contrib_graphs = True
            if self.total_contribution_amount < 0:
                self.reason = "negative"

class IndividualLandingView(EntityLandingView):
    label = 'individual'
    name = 'Individuals'
    sections = [
        IndividualContributionsLandingSection,
    ]

class LobbyistContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/lobbyist_landing_contributions.html'
    enabled = True

    def build_section_data(self):
        self.total_contribution_amount = sum([float(n['amount']) for n in self.data['state_fed_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.recipient_type_summary_data = self.prepare_parent_child_tree('recipient_type_summary')
        self.seat_summary_data = self.prepare_parent_child_tree('seat_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')
        self.in_state_out_of_state_summary_data = self.prepare_parent_child_tree('in_state_out_of_state_summary')
        
        if self.total_contribution_amount <= 0:
            self.suppress_contrib_graphs = True
            if self.total_contribution_amount < 0:
                self.reason = "negative"

class LobbyistLobbyingLandingSection(EntityLandingSection):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/lobbyist_landing_lobbying.html'
    enabled = False

class LobbyistLandingView(EntityLandingView):
    label = 'lobbyist'
    name = 'Lobbyists'
    sections = [
        LobbyistContributionsLandingSection,
        LobbyistLobbyingLandingSection,
    ]

class PolContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/pol_landing_contributions.html'
    enabled = False

class PolEarmarksLandingSection(EntityLandingSection):
    name = 'Earmarks'
    label = 'earmarks'
    template = 'entity_landing/pol_landing_earmarks.html'
    enabled = False

class PolLandingView(EntityLandingView):
    label = 'pol'
    name = 'Politicians'
    sections = [
        PolContributionsLandingSection,
        PolEarmarksLandingSection,
    ]
