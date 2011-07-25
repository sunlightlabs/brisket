from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import index, sitemap
from django.conf import settings
from influence import names
from django.template.defaultfilters import slugify
from django.http import HttpResponse
import os
from settings import api

class LandingSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    
    def items(self):
        return ["/", "/about/", "/contact/", "/about/methodology/campaign_finance", "/about/methodology/lobbying", "/organizations", "/politicians", "/people"]
    
    def location(self, item):
        return item
    
class EntityList:
    params = {}
    
    def __init__(self, type=None):
        if type:
            self.params['type'] = type
    
    def __len__(self):
        return api.entities.count(**self.params)
    
    def __getslice__(self, start, end):
        return api.entities.list(start, end, **self.params)
    

class EntitySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    limit = 5000
    
    entity_type=None
    
    def __init__(self):
        entity_type = self.entity_type or 'individual'
        self.cleaner = names._standardizers[entity_type]
    
    def clean(self, string):
        return slugify(self.cleaner(string))
        
    def items(self):
        return EntityList(self.entity_type)
    
    def location(self, item):
        return "/%s/%s/%s" % (item['type'], self.clean(item['name']), item['id'])

class IndividualSitemap(EntitySitemap):
    entity_type = "individual"

class OrganizationSitemap(EntitySitemap):
    entity_type = "organization"

class PoliticianSitemap(EntitySitemap):
    entity_type = "politician"

class IndustrySitemap(EntitySitemap):
    entity_type = "industry"

def index_wrapper(request, sitemaps):
    path = os.path.join(settings.MEDIA_ROOT, "sitemaps", "sitemap.xml")
    if os.path.exists(path):
        return HttpResponse(open(path), mimetype='application/xml')
    else:
        return index(request, sitemaps)

def sitemap_wrapper(request, sitemaps, section):
    path = os.path.join(settings.MEDIA_ROOT, "sitemaps", "sitemap-%s.xml" % section)
    if 'p' in request.GET:
        path += '_p_%s' % request.GET['p']
    if os.path.exists(path):
        return HttpResponse(open(path), mimetype='application/xml')
    else:
        return sitemap(request, sitemaps, section)

sitemaps = {
    'landing': LandingSitemap,
    'individual': IndividualSitemap,
    'organization': OrganizationSitemap,
    'politician': PoliticianSitemap,
    'industry': IndustrySitemap,
}
