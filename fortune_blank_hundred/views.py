from django.views.generic.base import TemplateView
from django.conf import settings
from influence.cache import cache
from collections import defaultdict
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

    numbers = set(['donor_total', 'lobby_total', 'influence_total', 'federal_biz_total', 'federal_aid_total', 'effective_tax_rate'])

    values = defaultdict(list)
    for row in data:
        weight = (int(row['rank']) - minr) / diffr
        color = [int(round((weight * minc[i]) + ((1 - weight) * maxc[i]))) for i in range(3)]
        hex_color = [('0' if channel < 16 else '') + hex(channel).split('x')[-1] for channel in color]
        row['color'] = ''.join(hex_color)

        # strip out hyphens from ie ids
        row['ie_id'] = row['ie_id'].replace('-', '')

        for key, value in row.items():
            if key in numbers:
                intval = None
                try:
                    intval = int(value)
                    values[key].append(intval)
                except ValueError:
                    pass

    averages = {'special_title': 'Average'}
    totals = {'special_title': 'Total'}
    for key, value_list in values.items():
        totals[key] = sum(value_list)
        averages[key] = int(round(float(totals[key]) / len(value_list)))

    return {
        'rows': data,
        'averages': averages,
        'totals': totals
    }

class FortuneIndexView(TemplateView):
    template_name = "fortune_blank_hundred/index.html"

    def get_context_data(self):
        table = get_table()

        return {'table': table['rows'] + [table['averages'], table['totals']]}