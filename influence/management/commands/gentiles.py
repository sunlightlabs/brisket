from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
import feedparser, re
from supertagging.calais import Calais
from influence import api
from util import catcodes
from influence.helpers import generate_label, pie_validate
import json

class Command(BaseCommand):
    help = 'Generates top news area on home page.'
    
    def handle(self, *args, **options):
        # grab significant entities
        entities = self.fetch_entities(args[1:])
        
        out = render_to_string(args[0], Context({'entities': entities}))
        print out        
    
    def fetch_entities(self, ids):
        entities = []
        for id in ids:
            entities.append(api.entity_metadata(id, cycle='-1'))
        
        # de-dupe entities
        seen_so_far = []
        out_entities = []
        for entity in entities:
            if entity['id'] not in seen_so_far:
                if entity['type'] == 'politician':
                    # grab some additional metadata
                    top_sectors = api.pol_sectors(entity['id'], cycle='-1')
                    
                    sectors_barchart_data = []
                    for record in top_sectors:
                        try:
                            sector_name = catcodes.sector[record['sector']]
                        except:
                            sector_name = 'Unknown (%s)' % record['sector']
                        sectors_barchart_data.append({
                            'key': generate_label(sector_name, max_length=30),
                            'value' : record['amount'],
                        })
                        entity['sectors_barchart_data'] = json.dumps(sectors_barchart_data[:5])
                
                elif entity['type'] == 'organization':
                    party_breakdown = api.org_party_breakdown(entity['id'], cycle='-1')
                    for key, values in party_breakdown.iteritems():
                        party_breakdown[key] = float(values[1])
                    if len(party_breakdown.keys()) < 2:
                        continue
                    entity['party_breakdown'] = json.dumps(pie_validate(party_breakdown))
                
                out_entities.append(entity)
                seen_so_far.append(entity['id'])
        
        return out_entities[:5]

def compare_entities(a, b):
    # first look at Calais's relevance metric
    relevance = cmp(a['relevance'], b['relevance'])
    if relevance != 0:
        return relevance
    
    # then, prefer people, organizations, and companies to everything else
#    best_types = {'Person': 1, 'Organization': 1, 'Company': 1}
#    type = cmp(best_types.get(a['_type'], 0), best_types.get(b['_type'], 0))
#    if type != 0:
#        return type
    
    # then, if they're both people, prefer political to non-political
    if a['_type'] == 'Person' and b['_type'] == 'Person':
        person_type = cmp(int(a['persontype'] == 'political'), int(b['persontype'] == 'political'))
        if person_type != 0:
            return person_type
    
    return 0