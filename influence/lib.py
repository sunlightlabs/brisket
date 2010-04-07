from django.conf import settings
import urllib2, urllib
import random
try:
    import json
except:
    import simplejson as json

class InfluenceNetworkBuilder(object):
    ''' Track a user's explorations through the data and maintain a
    graph-like structure with relationships between the entities of
    the various search results and clickthroughs.'''
    pass

class AggregatesAPI(object):
    ''' A thin wrapper around aggregates API calls. Not sure we'll
    keep this as a class, that might be overkill.'''
    def __init__(self):
        # grab the base url from settings and make sure it ends with a
        # trailing slash.
        self.base_url = settings.API_BASE_URL.strip('/')+'/'

    def entity_search(self, query):
        #make sure the query is properly encoded
        query_params = urllib.urlencode({'search': query})        
        url = self.base_url + 'entities.json?apikey=%s&' % settings.API_KEY
        api_call = url + query_params
        print api_call
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results

    def top_contributors(self, entity_id, **kwargs):
        valid_params = ['cycle', 'entity_types', 'limit']        
        for key in kwargs.keys():
            if key not in valid_params:
                raise Exception, "Invalid parameters to API call"

        kwargs['apikey'] = settings.API_KEY
        arguments = urllib.urlencode(kwargs)
        url = self.base_url + 'aggregates/entity/%s/contributors.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results

    def top_recipients(self, entity_id, **kwargs):
        valid_params = ['cycle', 'entity_types', 'limit']
        for key in kwargs.keys():
            if key not in valid_params:
                raise Exception, "Invalid parameters to API call"

        kwargs['apikey'] = settings.API_KEY
        arguments = urllib.urlencode(kwargs)
        url = self.base_url + 'aggregates/entity/%s/recipients.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results

    def top_industries(self, entity_id, **kwargs):
        valid_params = ['cycle', 'limit']
        for key in kwargs.keys():
            if key not in valid_params:
                raise Exception, "Invalid parameters to API call"

        kwargs['apikey'] = settings.API_KEY
        arguments = urllib.urlencode(kwargs)
        url = self.base_url + 'aggregates/entity/%s/contributors/industries.json?' % entity_id
        api_call = url + arguments
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results
        

    def entity_metadata(self, entity_id):
        arguments = 'entities/%s.json?apikey=%s' % (entity_id, settings.API_KEY)
        api_call = self.base_url.strip('/')+'/'+arguments        
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results
        
    def breakdown(self, direction, _type, cycle=None):
        ''' direction is either 'contributors' or 'recipients'. type
        can be one of party, instate, level, or source.'''
        if _type == 'party':
            label1 = 'Democrats'
            label2 = 'Republicans'
        elif _type == 'instate':
            label1 = 'In State'
            label2 = 'Out of State'
        elif _type == 'level':
            label1 = 'Federal'
            label2 = 'State'
        elif _type == 'source':
            label1 = 'Individuals'
            label2 = 'PACs'
        else: 
            print '_type argument to API.breakdown() function is invalid.'
            raise Exception, "Invalid 'type' argument to API call 'breakdown'"
        value1 = random.randint(0,100)
        fake_data = {
            label1 : str(value1),
            label2 : str(100 - value1)
            }
        return fake_data
        
