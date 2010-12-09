from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.http import Http404
import urllib2
import urllib
import re
try:
    import json
except:
    import simplejson as json


# to do:
# - remove parse_json flag. Should always be true


API_BASE_URL = settings.AGGREGATES_API_BASE_URL.strip('/')+'/'

# defaults of None don't mean that there is not default or no limit--
# it means that no parameter will be sent to the server, and the server
# will use its own default.
DEFAULT_LIMIT = None

DEFAULT_CYCLE = "-1" # -1 will return career totals.



class TransparencyDataAPI(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def _get_url_json(self, path, cycle=None, limit=None, parse_json=False, **params):
        """ Low level call that just adds the API key, retrieves the URL and parses the JSON. """

        if cycle:
            params.update({'cycle': cycle})
        if limit:
            params.update({'limit': limit})
        params.update({'apikey': settings.API_KEY})

        # avoid unicode errors
        if params.has_key('search'):
            params['search'] = params['search'].encode('ascii', 'ignore')

        try:
            fp = urllib2.urlopen(self.base_url + path + '?' + urllib.urlencode(params))

            if parse_json:
                return json.loads(fp.read())
            else:
                return fp.read()
        except urllib2.HTTPError, e:
            if e.code == 404:
                raise Http404
            else:
                raise e

    def entity_search(self, query):
        return self._get_url_json('entities.json', search=query, parse_json=True)

    _camp_fin_markers = ['contributor_count', 'recipient_count']
    _lobbying_markers = ['lobbying_count']
    _spending_markers = ['grant_count', 'loan_count', 'contract_count']
    _earmark_markers = ['earmark_count']

    def entity_metadata(self, entity_id):
        results = self._get_url_json('entities/%s.json' % entity_id, parse_json=True)

        results['years'] = self._entity_years(results['totals'], self._camp_fin_markers + self._lobbying_markers + self._spending_markers)
        results['camp_fin_years'] = self._entity_years(results['totals'], self._camp_fin_markers)
        results['lobbying_years'] = self._entity_years(results['totals'], self._lobbying_markers)
        results['spending_years'] = self._entity_years(results['totals'], self._spending_markers)
        results['earmark_years'] = self._entity_years(results['totals'], self._earmark_markers)

        return results

    def _entity_years(self, totals, keys):
        years = [year for (year, values) in totals.items() if any([v for (k,v) in values.items() if k in keys]) and year != "-1"]
        years.sort()
        if years:
            return dict(start=years[0], end=years[-1])
        else:
            return {}

    def entity_id_lookup(self, namespace, id, parse_json=True):
        return self._get_url_json('entities/id_lookup.json', namespace=namespace, id=id, parse_json=parse_json)


    def entity_count(self, type=None):
        params = {'count': 1}
        if type:
            params['type'] = type
        return int(self._get_url_json('entities/list.json', parse_json=True, **params)['count'])


    def entity_list(self, start, end, type=None):
        params = {'start': start, 'end': end}
        if type:
            params['type'] = type
        return self._get_url_json('entities/list.json', parse_json=True, **params)


    def pol_contributors(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/contributors.json' % entity_id, cycle, limit, parse_json)


    def indiv_org_recipients(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        ''' recipients from a single individual'''
        return self._get_url_json('aggregates/indiv/%s/recipient_orgs.json' % entity_id, cycle, limit, parse_json=parse_json)


    def indiv_pol_recipients(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        ''' recipients from a single individual'''
        return self._get_url_json('aggregates/indiv/%s/recipient_pols.json' % entity_id, cycle, limit, parse_json=parse_json)


    def org_recipients(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/recipients.json' % entity_id, cycle, limit, parse_json=parse_json)


    def pol_sectors(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/contributors/sectors.json' % entity_id, cycle, limit, parse_json)


    def pol_industries(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/contributors/industries.json' % entity_id, cycle, limit, parse_json)


    def org_party_breakdown(self, entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('aggregates/org/%s/recipients/party_breakdown.json' % entity_id, cycle, parse_json=parse_json)


    def org_level_breakdown(self, entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('aggregates/org/%s/recipients/level_breakdown.json' % entity_id, cycle, parse_json=parse_json)

    def pol_local_breakdown(self, entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/contributors/local_breakdown.json' % entity_id, cycle, parse_json=parse_json)

    def pol_contributor_type_breakdown(self, entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/contributors/type_breakdown.json' % entity_id, cycle, parse_json=parse_json)


    def indiv_party_breakdown(self, entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('aggregates/indiv/%s/recipients/party_breakdown.json' % entity_id, cycle, parse_json=parse_json)

    # lobbying firms hired by this org
    def org_registrants(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        ''' check to see if the entity hired any lobbyists'''
        return self._get_url_json('aggregates/org/%s/registrants.json' % entity_id, cycle, limit, parse_json=parse_json)

    # issues this org hired lobbying for
    def org_issues(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/issues.json' % entity_id, cycle, limit, parse_json=parse_json)

    # lobbyists who lobbied for this org (?)
    def org_lobbyists(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/lobbyists.json' % entity_id, cycle, limit, parse_json=parse_json)

    # which lobbying firms did this indiv work for
    def indiv_registrants(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/indiv/%s/registrants.json' % entity_id, cycle, limit, parse_json=parse_json)

    # issues this individual lobbied on
    def indiv_issues(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/indiv/%s/issues.json' % entity_id, cycle, limit, parse_json=parse_json)

    # who were the clients of the firms this indiv worked for
    def indiv_clients(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/indiv/%s/clients.json' % entity_id, cycle, limit, parse_json=parse_json)

    # issues this org was hired to lobby for
    def org_registrant_issues(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/registrant/issues.json' % entity_id, cycle, limit, parse_json=parse_json)

    # clients of the org as a registrant
    def org_registrant_clients(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/registrant/clients.json' % entity_id, cycle, limit, parse_json=parse_json)

    # lobbyists who work for this registrant (?)
    def org_registrant_lobbyists(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/registrant/lobbyists.json' % entity_id, cycle, limit, parse_json=parse_json)

    # top orgs in an industry
    def industry_orgs(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/industry/%s/orgs.json' % entity_id, cycle, limit, parse_json=parse_json)

    # top n lists
    def top_n_individuals(self, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/indivs/top_%s.json' % limit, cycle, parse_json=parse_json)

    def top_n_organizations(self, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/orgs/top_%s.json' % limit, cycle, parse_json=parse_json)

    def top_n_politicians(self, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/pols/top_%s.json' % limit, cycle, parse_json=parse_json)

    def top_n_industries(self, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/industries/top_%s.json' % limit, cycle, parse_json=parse_json)


    def org_sparkline(self, entity_id, cycle=DEFAULT_CYCLE):
        return self._get_url_json('aggregates/org/%s/sparkline.json' % entity_id, cycle)

    def org_sparkline_by_party(self, entity_id, cycle=DEFAULT_CYCLE):
        return  self._get_url_json('aggregates/org/%s/sparkline_by_party.json' % entity_id, cycle)

    def pol_sparkline(self, entity_id, cycle=DEFAULT_CYCLE):
        return self._get_url_json('aggregates/pol/%s/sparkline.json' % entity_id, cycle)

    def indiv_sparkline(self, entity_id, cycle=DEFAULT_CYCLE):
        return self._get_url_json('aggregates/indiv/%s/sparkline.json' % entity_id, cycle)

    def org_fed_spending(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/fed_spending.json' % entity_id, cycle, limit, parse_json=parse_json)

    def org_earmarks(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/org/%s/earmarks.json' % entity_id, cycle, limit, parse_json)

    def pol_earmarks(self, entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/earmarks.json' % entity_id, cycle, limit, parse_json)
    
    def pol_earmarks_local_breakdown(self, entity_id, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('aggregates/pol/%s/earmarks/local_breakdown.json' % entity_id, cycle, parse_json=parse_json)

    def candidates_by_location(self, location, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('entities/race/%s.json' % location, cycle, parse_json=parse_json)

    def election_districts(self, cycle=DEFAULT_CYCLE, parse_json=True):
        return self._get_url_json('entities/race/districts.json', cycle, parse_json=parse_json)


api = TransparencyDataAPI(API_BASE_URL)
