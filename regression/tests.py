from influence.api import TransparencyDataAPI



cycles = [2008, 2010, -1]

entity_methods = [TransparencyDataAPI.entity_metadata]


politician_methods = [
    TransparencyDataAPI.pol_contributors,
    TransparencyDataAPI.pol_industries,
    TransparencyDataAPI.pol_local_breakdown,
    TransparencyDataAPI.pol_contributor_type_breakdown
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


def cross(l, *rest):
    """ Return the cross product of lists. """
    if not rest:
        return [[x] for x in l]
    return [[x] + y for x in l for y in cross(rest[0], *rest[1:])]


def cross_calls(methods, *arg_lists):
    """ Return a list of all methods on all argument combinations.
    
        Each returned item is a pair of string label and function.
        The functions are not bound to an instance--they expect self as the only argument.
        
    """
    result = []
    for call in cross(methods, *arg_lists):
        method = call[0]
        args = call[1:]
        label = "%s(%s)" % (method.__name__, ", ".join(map(str, args)))
        func = lambda api: method(api, *args)
        result.append((label, func))

    return result

def run_regression(production, staging, methods):
    for (label, func) in methods:
        print "testing %s" % label
        
        production_result = func(production)
        staging_result = func(staging)
        
        if production_result == staging_result:
            print "identical"
        else:
            print "different"

def test_all():
    production_api = TransparencyDataAPI("http://transparencydata.com/api/1.0/")
    staging_api = TransparencyDataAPI("http://staging.influenceexplorer.com:8000/api/1.0/")

    calls = \
        cross_calls(politician_methods, politician_entities, cycles) + \
        cross_calls(organization_methods, organization_entities, cycles)

    run_regression(production_api, staging_api, calls)
    
