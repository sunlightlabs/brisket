from . import *
from influence.api import TransparencyDataAPI
from nose.plugins.attrib import attr
from nose.tools import assert_equal



cycles = [2008]


politician_methods = [
    TransparencyDataAPI.pol_contributors,
    TransparencyDataAPI.pol_industries,
    TransparencyDataAPI.pol_local_breakdown,
    TransparencyDataAPI.pol_contributor_type_breakdown,
    TransparencyDataAPI.pol_sparkline,
]

politician_entities = [
    '85ab2e74589a414495d18cc7a9233981', # Pelosi
    'f5afb921e5a94bf89dec093978a154e4', # Schwarzenegger
    '597e02e7d1b04d83976913da1b8e2998', # Clinton
]

organization_methods = [
    TransparencyDataAPI.org_recipients,
    TransparencyDataAPI.org_party_breakdown,
    TransparencyDataAPI.org_level_breakdown,
    TransparencyDataAPI.org_sparkline,
    TransparencyDataAPI.org_sparkline_by_party,
    TransparencyDataAPI.org_registrants,
    TransparencyDataAPI.org_issues,
    TransparencyDataAPI.org_lobbyists,
    TransparencyDataAPI.org_registrant_clients,
    TransparencyDataAPI.org_registrant_issues,
    TransparencyDataAPI.org_registrant_lobbyists,
    TransparencyDataAPI.org_fed_spending
]

organization_entities = [
    '878b4d98431344de88d8fb9757043a95', # Bank of America
    'fb702029157e4c7c887172eba71c66c5', # AFSCME
    'd5bc3b5e617b43ed89e73000de9ff379', # Van Scoyoc Assoc
]

individual_methods = [
    TransparencyDataAPI.indiv_org_recipients,
    TransparencyDataAPI.indiv_pol_recipients,
    TransparencyDataAPI.indiv_party_breakdown,
    TransparencyDataAPI.indiv_sparkline,
    TransparencyDataAPI.indiv_registrants,
    TransparencyDataAPI.indiv_issues,
    TransparencyDataAPI.indiv_clients,
]

individual_entities = [
    '56014031e60e4df6903025bd26e60b61', # Thomas Boggs
    '6a2a5d19dbea499d8e1db4dbddc12091', # Parker Collier
    '77905c714f74469db1db064dbc942dc9', # Edgar Bronfman Jr
]


industry_methods = [
    TransparencyDataAPI.industry_orgs
] + organization_methods

industry_entities = [
    'cdb3f500a3f74179bb4a5eb8b2932fa6', # Unknown
    'f50cf984a2e3477c8167d32e2b14e052', # Lawyers
]


entity_methods = [TransparencyDataAPI.entity_metadata]

entities = politician_entities + organization_entities + individual_entities + industry_entities

calls = \
    cross_calls(politician_methods, politician_entities, cycles) + \
    cross_calls(organization_methods, organization_entities, cycles) + \
    cross_calls(individual_methods, individual_entities, cycles) + \
    cross_calls(industry_methods, industry_entities, cycles) + \
    cross_calls(entity_methods, entities)


@attr('regression')
def test_all():
    production_api = TransparencyDataAPI("http://transparencydata.com/api/1.0/")
    staging_api = TransparencyDataAPI("http://staging.influenceexplorer.com:8000/api/1.0/")

    def runner(label, api_call):
        f = lambda: assert_equal(api_call(production_api), api_call(staging_api))
        f.description = label # used in nose's output
        return f

    for (label, api_call) in calls:
        yield runner(label, api_call)



