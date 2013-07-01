import base64, urllib, urllib2, struct, uuid, threading
import json, itertools
from datetime import datetime, timedelta
from django.utils.datastructures import SortedDict
from settings import api
from django.conf import settings

# contribution links
def _get_crp_url(type, standardized_name, ids, cycle=None):
    if type == 'industry':
        if "urn:crp:industry" not in ids:
            return None
        return "http://www.opensecrets.org/industries/indus.php?ind=%s" % ids['urn:crp:industry']
    elif (type == 'politician' and 'urn:crp:recipient' in ids) or type != 'politician':
        return "http://www.opensecrets.org/usearch/index.php?q=%s" % standardized_name
    return None

def _get_nimsp_url(type, standardized_name, ids, cycle):
    if type == 'organization' and 'urn:nimsp:organization' in ids:
        if cycle:
            return "http://www.followthemoney.org/database/topcontributor.phtml?u=%(id)s&y=%(cycle)s" % dict(id=ids['urn:nimsp:organization'], cycle=cycle)
        else:
            return "http://www.followthemoney.org/database/topcontributor.phtml?u=%(id)s" % dict(id=ids['urn:nimsp:organization'])
    elif type == 'politician' and 'urn:nimsp:recipient' in ids:
        return "http://www.followthemoney.org/database/uniquecandidate.phtml?uc=%(id)s" % dict(id=ids['urn:nimsp:recipient'])
    elif type == 'industry':
        return 'http://www.followthemoney.org/database/IndustryTotals.phtml'
    return None

def _get_td_url(type, standardized_name, ids, cycle):
    if type == 'industry':
        if "urn:crp:industry" not in ids:
            return None
        query_string = "contributor_industry=%s" % ids['urn:crp:industry']
    else:
        keywords = {'individual': 'contributor_ft', 'organization': 'organization_ft', 'politician': 'recipient_ft'}
        query_string = "%s=%s" % (keywords[type], standardized_name)
    if cycle:
        query_string += "&cycle=%s" % cycle
    query_string += '&general_transaction_type=standard'
    return "http://data.influenceexplorer.com/contributions/#%s" % base64.b64encode(query_string)

def get_contribution_links(type, standardized_name, namespaces_and_ids, cycle):
    """ Return a list of (label, url) pairs for an organization. """
    
    ids = dict([(item['namespace'], item['id']) for item in namespaces_and_ids])
    if cycle == '-1':
        cycle = None

    links = [
        dict(text='OpenSecrets.org', url=_get_crp_url(type, standardized_name, ids, cycle)),
        dict(text='FollowTheMoney.org', url=_get_nimsp_url(type, standardized_name, ids, cycle)),
        dict(text='campaign finance', url=_get_td_url(type, standardized_name, ids, cycle)),
    ]
    
    links = filter(lambda link: link['url'] is not None, links)

    return links


# grants and contracts links
def get_gc_links(standardized_name, cycle):
    # TD
    td_keywords = {}
    if cycle != '-1':
        td_keywords['fiscal_year'] = "%s|%s" % (int(cycle) - 1, cycle)
    
    grant_keywords = td_keywords.copy()
    grant_keywords.update({'recipient_ft': standardized_name})
    
    contract_keywords = td_keywords.copy()
    contract_keywords.update({'vendor_name': standardized_name})
    
    links = [
        dict(text='grant & loan', url="http://data.influenceexplorer.com/grants/#%s" % base64.b64encode(urllib.urlencode(grant_keywords))),
        dict(text='contract', url="http://data.influenceexplorer.com/contracts/#%s" % base64.b64encode(urllib.urlencode(contract_keywords)))
    ]
    
    # USA Spending
    usa_keywords = {'RecipientNameText': [standardized_name]}
    if cycle != '-1':
        usa_keywords['FiscalYear'] = [str(int(cycle) - 1), cycle]
    links.append(
        dict(text='USASpending.gov', url="http://usaspending.gov/search?query=&formFields=%s" % base64.b64encode(urllib.quote(json.dumps(usa_keywords))))
    )
    
    return links


def get_pogo_links(ids, standardized_name, cycle):
    links = []

    pogo_contractor_ids = filter(lambda s: s['namespace'] == 'urn:pogo:contractor', ids)
    if pogo_contractor_ids:
        links.append({'text': 'Federal Contractor Misconduct Database from POGO', 'url': 'http://www.contractormisconduct.org/index.cfm/1,73,221,html?ContractorID={0}'.format(pogo_contractor_ids[0]['id'])})

    td_params = {}
    if cycle != '-1':
        td_params['date_year'] = "{0}|{1}".format(int(cycle) - 1, cycle)

    td_params['contractor'] = standardized_name

    links.append({ 'text': 'contractor misconduct', 'url': 'http://data.influenceexplorer.com/contractor_misconduct/#{0}'.format(base64.b64encode(urllib.urlencode(td_params))) })
    return links


def get_epa_links(standardized_name, cycle):
    links = []

    td_params = {}
    if int(cycle) != -1:
        td_params['last_date'] = "><|{0}-01-01|{1}-12-31".format(str(int(cycle) - 1)[2:], str(cycle)[2:])

    td_params['defendants'] = standardized_name

    links.append({ 'text': 'EPA ECHO Enforcement Data', 'url': 'http://www.epa-echo.gov/echo/compliance_report_icis.html' })
    links.append({ 'text': 'EPA violations', 'url': 'http://data.influenceexplorer.com/epa_echo/#{0}'.format(base64.b64encode(urllib.urlencode(td_params))) })
    return links

def get_faca_links(standardized_name, cycle):
    links = []

    td_params = {}
    if int(cycle) != -1:
       td_params['year'] = "{0}|{1}".format(int(cycle) - 1, cycle)
    td_params['affiliation'] = standardized_name

    links.append({ 'text': 'advisory committee', 'url': 'http://data.influenceexplorer.com/faca/#{0}'.format(base64.b64encode(urllib.urlencode(td_params))) })
    return links


def get_lobbying_links(type, standardized_name, ids, cycle):
    links = []
    
    # Reporting's Lobbyist Registration Tracker
    if type in ('firm', 'client'):
        tracker_urls = filter(lambda s: s['namespace'] == 'urn:sunlight:lobbyist_registration_tracker_url', ids)
        if tracker_urls:
            links.append(
                dict(text='Lobbyist Registration Tracker', url="http://reporting.sunlightfoundation.com" + tracker_urls[0]['id'])
            )
    
    # TD
    td_types = {'firm': 'registrant_ft', 'lobbyist': 'lobbyist_ft', 'client': 'client_ft'}
    td_params = {}
    if cycle != '-1':
        td_params['year'] = "%s|%s" % (int(cycle) - 1, cycle)
    
    if type in td_types:
        td_params[td_types[type]] = standardized_name
        
        links.append(
            dict(text='lobbying', url="http://data.influenceexplorer.com/lobbying/#%s" % base64.b64encode(urllib.urlencode(td_params)))
        )
    
    # OpenSecrets
    os_types = {'firm': 'f', 'lobbyist': 'l', 'client': 'c'}
    if type == 'lobbyist':
        indiv_ids = filter(lambda s: s['namespace'] == 'urn:crp:individual', ids)
        if indiv_ids:
            os_params = {'lname': standardized_name, 'id': indiv_ids[0]['id']}
            if cycle != '-1':
                os_params['year'] = cycle
            links.append(
                dict(text='OpenSecrets.org', url="http://www.opensecrets.org/lobby/lobbyist.php?%s" % urllib.urlencode(os_params))
            )
    elif type == 'industry':
        industry_ids = filter(lambda s: s['namespace'] == 'urn:crp:industry', ids)
        if industry_ids:
            os_params = {'lname': industry_ids[0]['id']}
            td_params = {'industry': industry_ids[0]['id']}
            if cycle != '-1':
                os_params['year'] = cycle
                td_params['year'] = cycle
            links.append(
                dict(text='OpenSecrets.org', url="http://www.opensecrets.org/lobby/indusclient.php?%s" % urllib.urlencode(os_params))
            )
            links.append(
                dict(text='lobbying', url="http://data.influenceexplorer.com/lobbying/#%s" % base64.b64encode(urllib.urlencode(td_params)))
            )
    
    else:
        links.append(
            dict(text='OpenSecrets.org', url="http://www.opensecrets.org/lobby/lookup.php?%s" % urllib.urlencode({'type': os_types[type], 'lname': standardized_name}))
        )
    
    return links

def get_earmark_links(type, standardized_name, ids, cycle):
    links = []
    
    # TD
    td_types = {'organization': 'recipient', 'politician': 'member'}
    td_params = {}
    if cycle != '-1':
        td_params['year'] = "%s|%s" % (int(cycle) - 1, cycle)
    
    if type in td_types:
        td_params[td_types[type]] = standardized_name
        
        links.append(
            dict(text='earmarks', url="http://data.influenceexplorer.com/earmarks/#%s" % base64.b64encode(urllib.urlencode(td_params)))
        )
    
    # OpenSecrets
    politician_ids = filter(lambda s: s['namespace'] == 'urn:crp:recipient', ids)
    if politician_ids:
        os_params = {'cid': politician_ids[0]['id']}
        if cycle != '-1':
            os_params['year'] = cycle
        links.append(
            dict(text='OpenSecrets.org', url="http://www.opensecrets.org/politicians/earmarks.php?%s" % urllib.urlencode(os_params))
        )
    
    return links

from influence.cache import cache

def _pt_iter(crp_id):
    page = urllib2.urlopen("http://politicalpartytime.org/api/v1/event/?apikey=%s&format=json&beneficiaries__crp_id=%s" % (settings.API_KEY, crp_id))
    records = json.loads(page.read())
    yield records['objects']

    while records['meta']['next']:
        page = urllib2.urlopen("http://politicalpartytime.org%s" % records['meta']['next'])
        records = json.loads(page.read())
        yield records['objects']

@cache(seconds=86400)
def get_partytime_data(ids):
    politician_ids = filter(lambda s: s['namespace'] == 'urn:crp:recipient', ids)
    
    if not politician_ids:
        return (None, {'past': [], 'upcoming': []})
    
    try:
        records = list(itertools.chain.from_iterable(_pt_iter(politician_ids[0]['id'])))
    except:
        return None, None
    
    today = datetime.now()
    cutoff = today - timedelta(days=180)
    
    out = SortedDict()
    out['upcoming'] = sorted([dict(date=datetime.strptime(record['start_date'], '%Y-%m-%d'), **record) for record in records if record['start_date'] >= today.strftime('%Y-%m-%d')], key=lambda x: x['start_date'], reverse=True)[:3]
    out['past'] =sorted([dict(date=datetime.strptime(record['start_date'], '%Y-%m-%d'), **record) for record in records if record['start_date'] < today.strftime('%Y-%m-%d') and record['start_date'] >= cutoff.strftime('%Y-%m-%d')], key=lambda x: x['start_date'], reverse=True)[:(5 - len(out['upcoming']))]
    
    return ("http://politicalpartytime.org/pol/%s/" % politician_ids[0]['id'], out)

@cache(seconds=86400)
def get_lobbyist_tracker_data(ids):
    out = []
    tracker_urls = filter(lambda s: s['namespace'] == 'urn:sunlight:lobbyist_registration_tracker_url', ids)
    if tracker_urls:
        try:
            page = urllib2.urlopen("http://reporting.sunlightfoundation.com%s.json" % tracker_urls[0]['id'])
        except:
            return []
        records = json.loads(page.read())
        cutoff = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S')
        out = [record for record in records['registrations'] if record['received'] >= cutoff][:5]
        item_type = 'firm' if records['path'].startswith('/lobbying/firm') else 'client'
        id_fetch_type = 'registrant' if item_type == 'client' else 'client'
    for record in out:
        record['date'] = datetime.strptime(record['received'], '%Y-%m-%d %H:%M:%S')
        lookup = api.entities.id_lookup("urn:sunlight:lobbyist_registration_tracker_url", record[id_fetch_type]['path'])
        if lookup:
            record[id_fetch_type]['ie_path'] = '/organization/%s/%s' % (record[id_fetch_type]['path'].split('/')[-1], lookup[0]['id'])
    return out

@cache(seconds=86400)
def get_docketwrench_entity_data(entity_id, cycle=-1):
    dw = getattr(settings, "DOCKETWRENCH_URL", "http://docketwrench.sunlightfoundation.com/")
    icycle, scycle = int(cycle), str(cycle)
    page = urllib2.urlopen(dw + "api/1.0/entity/" + entity_id + "?format=json" + ("" if icycle == -1 else "&years=%s" % ",".join([str(icycle - 1), scycle])))
    return json.loads(page.read())

@cache(seconds=86400)
def get_docketwrench_entity_list():
    dw = getattr(settings, "DOCKETWRENCH_URL", "http://docketwrench.sunlightfoundation.com/")
    page = urllib2.urlopen(dw + "api/1.0/entity_list?format=binary")
    data = page.read()
    out = []
    for i in xrange(0, len(data), 16):
        # unpack UUID
        a, b = struct.unpack('>QQ', data[i:i+16])
        unpacked = (a << 64) | b
        out.append(uuid.UUID(int=unpacked).hex)
    return set(out)

# we'll keep a thread-local storage around as well, since even the pickling/unpickling of this giant thing is annoying and we'd prefer not to do it multiple times per request
_dw_local = threading.local()