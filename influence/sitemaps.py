from django.contrib.sitemaps import Sitemap
from influence.api import entity_count, entity_list
from django.conf import settings
from influence import helpers
from django.template.defaultfilters import slugify

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
        return entity_count(**self.params)
    
    def __getslice__(self, start, end):
        return entity_list(start, end, **self.params)
    

class EntitySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    limit = 5000
    
    entity_type=None
    
    def __init__(self):
        self.cleaner = helpers.__getattribute__('standardize_%s_name' % (self.entity_type if self.entity_type is not None else 'individual'))
    
    def clean(self, string):
        return slugify(self.cleaner(string))
        
    def items(self):
        return EntityList(self.entity_type)
    
    def location(self, item):
        return "/%s/%s/%s?cycle=%s" % (item['type'], self.clean(item['name']), item['id'], settings.LATEST_CYCLE)

class IndividualSitemap(EntitySitemap):
    entity_type = "individual"

class OrganizationSitemap(EntitySitemap):
    entity_type = "organization"

class PoliticianSitemap(EntitySitemap):
    entity_type = "politician"

sitemaps = {
    'landing': LandingSitemap,
    'individual': IndividualSitemap,
    'organization': OrganizationSitemap,
    'politician': PoliticianSitemap,
}