from django.conf import settings
from BeautifulSoup import BeautifulSoup
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

    def entity_metadata(self, entity_id, cycle):
        arguments = 'entities/%s.json?apikey=%s&cycle=%s' % (entity_id, settings.API_KEY, cycle)
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


    def as_client(self, org_name, cycle):
        ''' check to see if org_name hired (was the client of) any
        lobbyists'''
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'client_ft': org_name,
                                      'year': cycle,
                                      })
        url = self.base_url + 'lobbying.json?'
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)

    def as_registrant(self, org_name, cycle):
        ''' check to see if org_name hired (was the client of) any
        lobbyists'''
        arguments = urllib.urlencode({'apikey': settings.API_KEY, 
                                      'registrant_ft': org_name,
                                      'year': cycle,
                                      })
        url = self.base_url + 'lobbying.json?'
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return self.remove_unicode(results)


def get_bioguide_id(full_name):
    ''' attempt to determine the bioguide_id of this legislastor, or
    return None. removes some basic formatting and trailing party
    designators'''
    # do some basic sanity checking on the name passed in
    if full_name.rfind('(D)') > -1:
        full_name = full_name.strip('(D)').strip()
    elif full_name.rfind('(R)') > -1:
        full_name = full_name.strip('(R)').strip()

    # gracefully handle slug-formatted strings
    name = full_name.replace('-',' ')

    arguments = urllib.urlencode({'apikey': settings.SUNLIGHT_API_KEY, 
                                  'name': name,
                                  'all_legislators': 1,
                                  })    
    url = "http://services.sunlightlabs.com/api/legislators.search.json?"
    api_call = url + arguments
    print api_call
    fp = urllib2.urlopen(api_call)
    js = json.loads(fp.read())    
    try:
        #legislators.search method returns a set of results, sorted by
        #decreasing 'quality' of the result. take here the best
        #match-- the first one.
        bioguide_id = js['response']['results'][0]['result']['legislator']['bioguide_id']
    except:
        bioguide_id = None
    print bioguide_id
    return bioguide_id

def get_capitol_words(full_name, cycle, limit):
    # get bioguide
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


def politician_picture_url(full_name):
    ''' we aren't using this directly right now, but might in the
    future so will leave it in for now.'''
    bioguide_id = get_bioguide_id(full_name)    
    if not bioguide_id:
        print 'No bioguide_id found for legislator %s' % full_name
        return None
    print 'bioguide_id for %s: %s' % (full_name, bioguide_id)
    return "http://assets.sunlightfoundation.com/moc/100x125/%s.jpg" % bioguide_id

def politician_meta(full_name):
    bioguide_id = get_bioguide_id(full_name)
    
    if not bioguide_id:
        return None

    photo_url = "http://assets.sunlightfoundation.com/moc/100x125/%s.jpg" % bioguide_id
    
    # scrape congress's bioguide site for years of service and official bio
    html = urllib2.urlopen("http://bioguide.congress.gov/scripts/biodisplay.pl?index=%s" % bioguide_id).read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    yrs_of_service = soup.findAll('table')[1].find('tr').findAll('td')[1].findAll('font')[2].next.next.next.strip()
    bio_a = soup.findAll('table')[1].find('tr').findAll('td')[1].find('p').find('font').extract().renderContents()
    bio_b = soup.findAll('table')[1].find('tr').findAll('td')[1].find('p').renderContents()
    biography = bio_a.strip()+' '+bio_b.strip()

    # other metadata - from sunlightlabs services
    arguments = urllib.urlencode({'apikey': settings.SUNLIGHT_API_KEY, 
                                  'bioguide_id': bioguide_id,
                                  'all_legislators': 1,
                                  })    
    url = "http://services.sunlightlabs.com/api/legislators.get.json?"
    api_call = url + arguments
    print api_call
    fp = urllib2.urlopen(api_call)
    js = json.loads(fp.read())    
    meta = js['response']['legislator']
    
    # append additional info and return
    meta['photo_url'] = photo_url
    meta['yrs_of_service'] = yrs_of_service
    meta['biography'] = biography
    return meta


