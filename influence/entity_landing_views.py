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
        amount = sum([float(n['amount']) for n in self.data['party_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.pol_group_summary_data = self.prepare_parent_child_tree('pol_group_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')

        if amount <= 0:
            self.suppress_contrib_graphs = True
            if amount < 0:
                self.reason = "negative"

class OrgLobbyingLandingSection(Section):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/org_landing_lobbying.html'

class OrgRegulationsLandingSection(Section):
    name = 'Regulations'
    label = 'regulations'
    template = 'entity_landing/org_landing_regulations.html'
    enabled = False

class OrgEarmarksLandingSection(Section):
    name = 'Earmarks'
    label = 'earmarks'
    template = 'entity_landing/org_landing_earmarks.html'
    enabled = False

class OrgGrantsAndContractsLandingSection(Section):
    name = 'Federal Spending'
    label = 'grants_and_contracts'
    template = 'entity_landing/org_landing_grants_and_contracts.html'
    enabled = False

class OrgContractorMisconductLandingSection(Section):
    name = 'Contractor Misconduct'
    label = 'contractor_misconduct'
    template = 'entity_landing/org_landing_contractor_misconduct.html'
    enabled = False

class OrgEpaEchoLandingSection(Section):
    name = 'EPA Violations'
    label = 'epa_echo'
    template = 'entity_landing/org_landing_epa_echo.html'
    enabled = False

class OrgFacaLandingSection(Section):
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

class PolGroupContributionsLandingSection(Section):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/pol_group_landing_contributions.html'
    enabled = False

class PolGroupLobbyingLandingSection(Section):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/pol_group_landing_lobbying.html'
    enabled = False

class PolGroupRegulationsLandingSection(Section):
    name = 'Regulations'
    label = 'regulations'
    template = 'entity_landing/pol_group_landing_regulations.html'
    enabled = False

class PolGroupFacaLandingSection(Section):
    name = 'Advisory Committees'
    label = 'faca'
    template = 'entity_landing/pol_group_landing_faca.html'
    enabled = False

class PolGroupLandingView(EntityLandingView):
    label = 'pol_group'
    name = 'Political Groups'
    sections = [
        PolGroupContributionsLandingSection,
        PolGroupLobbyingLandingSection,
        PolGroupRegulationsLandingSection,
        PolGroupFacaLandingSection,
    ]
    enabled = False

class LobbyingFirmContributionsLandingSection(Section):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/lobbying_firm_landing_contributions.html'
    enabled = False

class LobbyingFirmLobbyingLandingSection(Section):
    name = 'Lobbying'
    label = 'lobbying'
    template = 'entity_landing/lobbying_firm_landing_lobbying.html'
    enabled = False

class LobbyingFirmRegulationsLandingSection(Section):
    name = 'Regulations'
    label = 'regulations'
    template = 'entity_landing/lobbying_firm_landing_regulations.html'
    enabled = False

class LobbyingFirmFacaLandingSection(Section):
    name = 'Advisory Committees'
    label = 'faca'
    template = 'entity_landing/lobbying_firm_landing_faca.html'
    enabled = False

class LobbyingFirmLandingView(EntityLandingView):
    label = 'lobbying_firm'
    name = 'Lobbying Firms'
    sections = [
        LobbyingFirmContributionsLandingSection,
        LobbyingFirmLobbyingLandingSection,
        LobbyingFirmRegulationsLandingSection,
        LobbyingFirmFacaLandingSection,
    ]

### People ###
class ContributorContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/contributor_landing_contributions.html'
    enabled = True

    def build_section_data(self):
        amount = sum([float(n['amount']) for n in self.data['party_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.recipient_type_summary_data = self.prepare_parent_child_tree('recipient_type_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')

class ContributorLandingView(EntityLandingView):
    label = 'contributor'
    name = 'Contributors'
    sections = [
        ContributorContributionsLandingSection,
    ]

class LobbyistContributionsLandingSection(EntityLandingSection):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/lobbyist_landing_contributions.html'
    enabled = True

    def build_section_data(self):
        amount = sum([float(n['amount']) for n in self.data['party_summary']])

        self.party_summary_data = self.prepare_parent_child_tree('party_summary')
        self.recipient_type_summary_data = self.prepare_parent_child_tree('recipient_type_summary')
        self.state_fed_summary_data = self.prepare_parent_child_tree('state_fed_summary')

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

class PolContributionsLandingSection(Section):
    name = 'Campaign Finance'
    label = 'contributions'
    template = 'entity_landing/pol_landing_contributions.html'
    enabled = False

class PolEarmarksLandingSection(Section):
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
