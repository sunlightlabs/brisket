from django.contrib.sitemaps import Sitemap

class LandingSitemap(Sitemap):
    chagefreq = "monthly"
    priority = 0.8
    
    def items(self):
        return ["/", "/about/", "/contact/", "/about/methodology/campaign_finance", "/about/methodology/lobbying", "/organizations", "/politicians", "/people"]
    
    def location(self, item):
        return item