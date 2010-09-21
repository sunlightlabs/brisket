from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.http import Http404
import helpers
import urllib2
import urllib
import re
try:
    import json
except:
    import simplejson as json


API_BASE_URL = settings.AGGREGATES_API_BASE_URL.strip('/')+'/'

# defaults of None don't mean that there is not default or no limit--
# it means that no parameter will be sent to the server, and the server
# will use its own default.
DEFAULT_CYCLE = "-1" # -1 will return career totals.
DEFAULT_LIMIT = None


def get_url_json(path, cycle=None, limit=None, parse_json=False, **params):
    """ Low level call that just adds the API key, retrieves the URL and parses the JSON. """

    if cycle:
        params.update({'cycle': cycle})
    if limit:
        params.update({'limit': limit})
    params.update({'apikey': settings.API_KEY})

    try:
        fp = urllib2.urlopen(API_BASE_URL + path + '?' + urllib.urlencode(params))
    
        if parse_json:
            return json.loads(fp.read())
        else:
            return fp.read()
    except urllib2.HTTPError, e:
        raise Http404

def entity_search(query):
    return get_url_json('entities.json', search=query, parse_json=True)


def entity_metadata(entity_id, cycle=DEFAULT_CYCLE):
    results = get_url_json('entities/%s.json' % entity_id, cycle, parse_json=True)
    career = results['totals'].keys()
    career.sort()
    # start at index 1 to skip over the -1 for 'all cycles'
    if len(career):
        results['career'] = {'start': career[1], 'end': career[-1]}
    else:
        results['career'] = {}

    # lobbying career
    lobbying_career = [k for (k,v) in results['totals'].items() if v['lobbying_count']]
    lobbying_career.sort()
    # start at index 1 to skip over the -1 for 'all cycles'
    if len(lobbying_career):
        results['lobbying_career'] = {'start': lobbying_career[1], 'end': lobbying_career[-1]}
    else:
        results['lobbying_career'] = {}

    return results


def entity_id_lookup(namespace, id):
    return get_url_json('entities/id_lookup.json', namespace=namespace, id=id)


def entity_count(type=None):
    params = {'count': 1}
    if type:
        params['type'] = type
    return int(get_url_json('entities/list.json', parse_json=True, **params)['count'])


def entity_list(start, end, type=None):
    params = {'start': start, 'end': end}
    if type:
        params['type'] = type
    return get_url_json('entities/list.json', parse_json=True, **params)

    
def pol_contributors(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/pol/%s/contributors.json' % entity_id, cycle, limit, parse_json)


def indiv_org_recipients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    ''' recipients from a single individual'''
    return get_url_json('aggregates/indiv/%s/recipient_orgs.json' % entity_id, cycle, limit, parse_json=parse_json)


def indiv_pol_recipients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    ''' recipients from a single individual'''
    return get_url_json('aggregates/indiv/%s/recipient_pols.json' % entity_id, cycle, limit, parse_json=parse_json)


def org_recipients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/recipients.json' % entity_id, cycle, limit, parse_json=parse_json)


def pol_sectors(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/pol/%s/contributors/sectors.json' % entity_id, cycle, limit, parse_json)


def org_party_breakdown(entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
    return get_url_json('aggregates/org/%s/recipients/party_breakdown.json' % entity_id, cycle, parse_json=parse_json)


def org_level_breakdown(entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
    return get_url_json('aggregates/org/%s/recipients/level_breakdown.json' % entity_id, cycle, parse_json=parse_json)


def pol_local_breakdown(entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
    return get_url_json('aggregates/pol/%s/contributors/local_breakdown.json' % entity_id, cycle, parse_json=parse_json)


def pol_contributor_type_breakdown(entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
    return get_url_json('aggregates/pol/%s/contributors/type_breakdown.json' % entity_id, cycle, parse_json=parse_json)


def indiv_party_breakdown(entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
    return get_url_json('aggregates/indiv/%s/recipients/party_breakdown.json' % entity_id, cycle, parse_json=parse_json)

# lobbying firms hired by this org
def org_registrants(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    ''' check to see if the entity hired any lobbyists'''
    return get_url_json('aggregates/org/%s/registrants.json' % entity_id, cycle, limit, parse_json=parse_json)

# issues this org hired lobbying for
def org_issues(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/issues.json' % entity_id, cycle, limit, parse_json=parse_json)

# lobbyists who lobbied for this org (?)
def org_lobbyists(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/lobbyists.json' % entity_id, cycle, limit, parse_json=parse_json)

# full-text grant search
def org_grants(name, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    params = {'recipient_ft': name, 'limit':limit, 'parse_json': parse_json}
    if cycle != "-1":
        params['fiscal_year'] = "%s|%s" % (int(cycle) - 1, cycle)
    return get_url_json('grants.json', **params)

# full-text contract search
def org_contracts(name, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    params = {'vendor_name': name, 'limit':limit, 'parse_json': parse_json}
    if cycle != "-1":
        params['fiscal_year'] = "%s|%s" % (int(cycle) - 1, cycle)
    return get_url_json('contracts.json', **params)

# which lobbying firms did this indiv work for
def indiv_registrants(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/indiv/%s/registrants.json' % entity_id, cycle, limit, parse_json=parse_json)

# issues this individual lobbied on
def indiv_issues(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/indiv/%s/issues.json' % entity_id, cycle, limit, parse_json=parse_json)

# who were the clients of the firms this indiv worked for
def indiv_clients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/indiv/%s/clients.json' % entity_id, cycle, limit, parse_json=parse_json)

# issues this org was hired to lobby for
def org_registrant_issues(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/registrant/issues.json' % entity_id, cycle, limit, parse_json=parse_json)

# clients of the org as a registrant
def org_registrant_clients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/registrant/clients.json' % entity_id, cycle, limit, parse_json=parse_json)

# lobbyists who work for this registrant (?)
def org_registrant_lobbyists(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/registrant/lobbyists.json' % entity_id, cycle, limit, parse_json=parse_json)

# top n lists
def top_n_individuals(cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/indivs/top_%s.json' % limit, cycle, parse_json=parse_json)

def top_n_organizations(cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/orgs/top_%s.json' % limit, cycle, parse_json=parse_json)

def top_n_politicians(cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/pols/top_%s.json' % limit, cycle, parse_json=parse_json)


def org_sparkline(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/org/%s/sparkline.json' % entity_id, cycle)

def org_sparkline_by_party(entity_id, cycle=DEFAULT_CYCLE):
    return  get_url_json('aggregates/org/%s/sparkline_by_party.json' % entity_id, cycle)

def pol_sparkline(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/pol/%s/sparkline.json' % entity_id, cycle)

def indiv_sparkline(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/indiv/%s/sparkline.json' % entity_id, cycle)
    
def org_fed_spending(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
    return get_url_json('aggregates/org/%s/fed_spending.json' % entity_id, cycle, limit, parse_json=parse_json)

