# Create your views here.
import json, csv, os
from django.http import HttpResponse
from influence.names import standardize_name

from django.contrib.localflavor.us.us_states import US_STATES
backwards_states = dict([(s[1].upper(), s[0]) for s in US_STATES])

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
    transforms = {
        'name': lambda n: standardize_name(n, 'politician').__str__()
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
                row[key] = transforms[key](row[key])
        
        out.append(row)
    
    return HttpResponse(json.dumps(out), mimetype="application/json")
