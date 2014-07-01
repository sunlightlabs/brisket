from django.views.generic.base import TemplateView
from django.conf import settings
from influence.cache import cache
import csv, urllib2

MIN_COLOR = "A0B73B"
MAX_COLOR = "5A7F26"

@cache(seconds=8600)
def get_table():
    url = getattr(settings, "FORTUNE_BLANK_HUNDRED_CSV")
    if not url:
        return []
    data = list(csv.DictReader(urllib2.urlopen(url)))
    
    # add in hex colors
    minc = [int(MIN_COLOR[i*2:(i*2)+2], 16) for i in range(3)]
    maxc = [int(MAX_COLOR[i*2:(i*2)+2], 16) for i in range(3)]

    ranks = [int(row['rank']) for row in data]
    minr = min(ranks)
    maxr = max(ranks)
    diffr = float(maxr - minr)

    for row in data:
        weight = (int(row['rank']) - minr) / diffr
        color = [int(round((weight * minc[i]) + ((1 - weight) * maxc[i]))) for i in range(3)]
        hex_color = [('0' if channel < 16 else '') + hex(channel).split('x')[-1] for channel in color]
        row['color'] = ''.join(hex_color)

        # strip out hyphens from ie ids
        row['ie_id'] = row['ie_id'].replace('-', '')

    return data

class FortuneIndexView(TemplateView):
    template_name = "fortune_blank_hundred/index.html"

    def get_context_data(self):
        return {'table': get_table()}