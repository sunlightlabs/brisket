from django.conf import settings
import urllib2, urllib
import random
try:
    import json
except:
    import simplejson as json

class APIUtil(object):
    def remove_unicode(self, data):
        ''' converts a dictionary or list of dictionaries with unicode
        keys or values to plain string keys'''
        if isinstance(data, dict):
            plain = {}
            for k,v in data.iteritems():
                k = self.remove_unicode(k)
                v = self.remove_unicode(v)
                plain[k] = v
            return plain
        if isinstance(data, list):
            plain = []
            for record in data:
                plain.append(self.remove_unicode(record))
            return plain
        if isinstance(data,unicode):
            return str(data)
        else: return data
    

class AggregatesAPI(APIUtil):
    ''' A thin wrapper around aggregates API calls. Not sure we'll
    keep this as a class, that might be overkill.'''
    def __init__(self):
        # grab the base url from settings file and make sure it ends
        # with a trailing slash (since it's a user-specified value).
        self.base_url = settings.AGGREGATES_API_BASE_URL.strip('/')+'/'

    def entity_search(self, query):
        #make sure the query is properly encoded
        query_params = urllib.urlencode({'search': query})        
        url = self.base_url + 'entities.json?apikey=%s&' % settings.API_KEY
        api_call = url + query_params
        print api_call
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results

    def pol_contributors(self, entity_id, contributor_type, cycle='2010'):
        arguments = urllib.urlencode({'type': contributor_type,
                                      'cycle': cycle,
                                      'apikey': settings.API_KEY})
        url = self.base_url + 'aggregates/pol/%s/contributors.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)

    def indiv_recipients(self, entity_id, recipient_types, cycle='2010', limit=10):
        ''' recipients from a single individual'''
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'type': recipient_types,
                                      'cycle': cycle,
                                      'limit': limit})

        url = self.base_url + 'aggregates/indiv/%s/recipients.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)


    def org_recipients(self, entity_id, **kwargs):
        valid_params = ['cycle', 'recipient_types', 'limit']
        for key in kwargs.keys():
            if key not in valid_params:
                raise Exception, "Invalid parameters to API call"
        kwargs['apikey'] = settings.API_KEY
        arguments = urllib.urlencode(kwargs)
        url = self.base_url + 'aggregates/org/%s/recipients.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)

    def top_sectors(self, entity_id, **kwargs):
        valid_params = ['cycle', 'limit']
        for key in kwargs.keys():
            if key not in valid_params:
                raise Exception, "Invalid parameters to API call"

        kwargs['apikey'] = settings.API_KEY
        arguments = urllib.urlencode(kwargs)
        url = self.base_url + 'aggregates/pol/%s/contributors/sectors.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)
        

    def contributions_by_sector(self, entity_id, sector_id):
        arguments = urllib.urlencode({'apikey': settings.API_KEY})
        url = self.base_url + 'aggregates/pol/%s/contributors/sectors/%s/industries.json?' % (entity_id, industry_id)
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)

    def entity_metadata(self, entity_id):
        arguments = 'entities/%s.json?apikey=%s' % (entity_id, settings.API_KEY)
        api_call = self.base_url.strip('/')+'/'+arguments        
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results
        
    def org_breakdown(self, entity_id, breakdown_type, cycle='2010'):
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'type': breakdown_type,
                                      'cycle': cycle})
        url = self.base_url + 'aggregates/org/%s/recipients/breakdown.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)

    def pol_breakdown(self, entity_id, breakdown_type, cycle='2010'):
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'type': breakdown_type,
                                      'cycle': cycle})
        url = self.base_url + 'aggregates/pol/%s/contributors/breakdown.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())        
        return self.remove_unicode(results)

    def indiv_breakdown(self, entity_id, breakdown_type, cycle='2010'):
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'type': breakdown_type,
                                      'cycle': cycle})
        url = self.base_url + 'aggregates/indiv/%s/recipients/breakdown.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)
            

class LobbyingAPI(APIUtil):
    ''' A thin wrapper around aggregates API calls. Not sure we'll
    keep this as a class, that might be overkill.'''
    def __init__(self):
        # grab the base url from settings file and make sure it ends
        # with a trailing slash (since it's a user-specified value).
        self.base_url = settings.LOBBYING_API_BASE_URL.strip('/')+'/'


    def by_client(self, org_name, cycle):
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'client_ft': org_name,
                                      'year': cycle,
                                      })
        url = self.base_url + 'lobbying.json?'
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)


def get_bioguide_id(full_name):
    arguments = urllib.urlencode({'apikey': settings.SUNLIGHT_API_KEY, 
                                  'name': full_name,
                                  'all_legislators': 1,
                                  })    
    url = "http://services.sunlightlabs.com/api/legislators.search.json?"
    api_call = url + arguments
    print api_call
    fp = urllib2.urlopen(api_call)
    js = json.loads(fp.read())    
    try:
        bioguide_id = js['response']['results'][0]['result']['legislator']['bioguide_id']
    except:
        bioguide_id = None
    print bioguide_id
    return bioguide_id

def get_capitol_words(full_name, cycle, limit):
    # get bioguide
    if full_name.rfind('(D)') > -1:
        full_name = full_name.strip('(D)').strip()
    elif full_name.rfind('(R)') > -1:
        full_name = full_name.strip('(R)').strip()
    bioguide_id = get_bioguide_id(full_name)

    if not bioguide_id:
        print 'No bioguide_id found for legislator %s' % full_name
        return None
    
    url = "http://capitolwords.org/api/lawmaker/%s/%s/top%d.json" % (bioguide_id, cycle, limit)
    try:
        fp = urllib2.urlopen(url)
        results = json.loads(fp.read())
        print results #list
        # may want to remove unicode here eventually, too. 
        return results
    except Exception, e:
        print 'Error retrieving capitol words'
        print url
        print e
        return None
