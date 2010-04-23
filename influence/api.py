from django.conf import settings
import urllib2, urllib
import random
try:
    import json
except:
    import simplejson as json

class AggregatesAPI(object):
    ''' A thin wrapper around aggregates API calls. Not sure we'll
    keep this as a class, that might be overkill.'''
    def __init__(self):
        # grab the base url from settings file and make sure it ends
        # with a trailing slash (since it's a user-specified value).
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
