from django.conf import settings
import urllib2, urllib
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
        self.base_url = settings.API_BASE_URL

    def entity_search(self, query):
        arguments = 'entities.json?search=%s&apikey=%s' % (query, settings.API_KEY)
        api_call = self.base_url.strip('/')+'/'+arguments
        print api_call
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results


    def top_contributors(self, entity_id, entity_types=None):
        # entity_types can be one or more of individual, pac (and
        # eventually industry and employer). do some type checking:
        if entity_types:
            arguments = ('aggregates/entity/%s/contributors.json?type=%s&apikey=%s' % 
                         (entity_id, _type, settings.API_KEY))
        else:
            arguments = ('aggregates/entity/%s/contributors.json?apikey=%s' % 
                         (entity_id, settings.API_KEY))            
        api_call = self.base_url.strip('/')+'/'+arguments        
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results

    def top_recipients(self, entity_id, entity_types=None):
        arguments = 'aggregates/entity/%s/recipients.json?apikey=%s' % (entity_id, settings.API_KEY)
        api_call = self.base_url.strip('/')+'/'+arguments        
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results


    def entity_metadata(self, entity_id):
        arguments = 'entities/%s.json?apikey=%s' % (entity_id, settings.API_KEY)
        api_call = self.base_url.strip('/')+'/'+arguments        
        fp = urllib2.urlopen(api_call)
        results = json.loads(fp.read())
        return results
        
        
