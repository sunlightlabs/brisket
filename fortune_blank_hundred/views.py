from django.views.generic.base import TemplateView
from django.conf import settings
from influence.cache import cache
import csv, urllib2

MIN_COLOR = "ffffff"
MAX_COLOR = "000000"

@cache(seconds=8600)
def get_table():
    url = getattr(settings, "FORTUNE_BLANK_HUNDRED_CSV")
    if not url:
        return []
    data = list(csv.DictReader(urllib2.urlopen(url)))
    
    # add in hex colors
    minc = [int(MIN_COLOR[i*2:(i*2)+2], 16) for i in range(3)]
    maxc = [int(MAX_COLOR[i*2:(i*2)+2], 16) for i in range(3)]

    return data

class FortuneIndexView(TemplateView):
    template_name = "fortune_blank_hundred/index.html"

    def get_context_data(self):
        return {'table': get_table()}