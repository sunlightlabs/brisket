from django.core.management.base import BaseCommand, CommandError
from influence.sitemaps import sitemaps
from django.contrib.sitemaps.views import *
from django.conf import settings
from django.http import HttpRequest
import os, re, urlparse

class Command(BaseCommand):
    help = "Generates static sitemap.xml files."
    
    def handle(self, *args, **options):
        directory = os.path.join(settings.MEDIA_ROOT, 'sitemaps')
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        # make fake request
        r = HttpRequest()
        
        # do the sitemap index
        response = index(r, sitemaps)
        f = open(os.path.join(directory, 'sitemap.xml'), 'w')
        f.write(response.content)
        f.close()
        
        # do all of the individual sitemaps
        maps = re.findall(r'<loc>(.*?)</loc>', response.content)
        for map in maps:
            url = urlparse.urlparse(map)
            r.GET = dict(urlparse.parse_qsl(url.query))
            section = url.path.split("-").pop().split(".").pop(0)
            
            filename = os.path.join(directory, url.path[1:])
            if ('p' in r.GET):
                filename += "_p_%s" % r.GET['p']
            
            response = sitemap(r, sitemaps, section)
            f = open(filename, 'w')
            f.write(response.content)
            f.close()