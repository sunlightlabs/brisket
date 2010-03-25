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
        results_annotated = []
        for (id_, name, count, total_given, total_received) in results:
            results_annotated.append({
                    'id': id_,
                    'name': name,
                    'count': count,
                    'total_given': float(total_given),
                    'total_received': float(total_received)
                    })
        return results_annotated

