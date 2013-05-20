# Create your views here.
import json, csv, os
from django.http import HttpResponse
from influence.helpers import standardize_name
from django.template.defaultfilters import slugify

from django.views.generic.simple import direct_to_template

from django_localflavor_us.us_states import US_STATES
backwards_states = dict([(s[1].upper(), s[0]) for s in US_STATES])

from settings import api

def get_json(request, file):
    substitutions = {
        'party': {
            'Dem': 'Democrat',
            'Rep': 'Republican',
            'Ind': 'Independent',
            'DEM': 'Democrat',
            'REP': 'Republican',
            'IND': 'Independent',
        },
        'state': backwards_states,
        'incumbency': {
            'Opn': 'Open',
            'Chl': 'Challenger',
            'Inc': 'Incumbent',
        },
    }
    
    def fix_name(n):
        name = standardize_name(n, 'politician')
        str_name = name.__str__()
        return { 'name': str_name, 'last_name': name.last, 'slug': slugify(str_name) }
    
    transforms = {
        'name': fix_name
    }
    out = []
    
    reader_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file), 'rb')
    reader = csv.DictReader(reader_file)
    
    for row in reader:
        for key in row.keys():
            if key in substitutions:
                if row[key] in substitutions[key]:
                    row[key] = substitutions[key][row[key]]
            elif key in transforms:
                row.update(transforms[key](row[key]))
        
        out.append(row)
    
    return HttpResponse(json.dumps(out), mimetype="application/json")

def bundling(request):
    return direct_to_template(
        request,
        'fec/bundling.html',
        extra_context = {
            'recipients': api._get_url_json('aggregates/lobbyist_bundling/recipients.json'),
            'firms': api._get_url_json('aggregates/lobbyist_bundling/firms.json')
        }
    )
