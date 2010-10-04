from influence.frontpage.top_news import TopNews
from influence import api
import json
from influence.frontpage import register_region
from influence.helpers import generate_label, pie_validate, standardize_organization_name
from django.template.defaultfilters import striptags

class Stories(TopNews):
    name = 'stories'
    url = 'http://feeds.feedburner.com/SunlightFoundationReportingGroup'
    to_parse = 5
    to_return = 1
    
    def process_entries(self, pg_entries):
        for entry in pg_entries:
            entry['entities'] = sorted(filter(lambda s: s['tdata_id'] is not None, entry['pg_struct']['entities']), cmp=lambda a, b: cmp(a['relevance'], b['relevance']), reverse=True)
            entry['text'] = "<br /><br />".join([striptags(para) for para in entry['pg_struct']['source_content'].split('</p>')[1:3]])
            
        # pick the one with the most entities referenced
        entry = sorted(pg_entries, cmp=lambda a, b: cmp(len(a['entities']), len(b['entities'])), reverse=True)[0]
        entry['entities'] = entry['entities'][:2]
        for entity in entry['entities']:
            entity['metadata'] = api.entity_metadata(entity['tdata_id'], cycle='-1')
        
        # de-dupe entities
        seen_so_far = []
        for pg_entity in entry['entities']:
            entity = pg_entity['metadata']
            if entity['id'] not in seen_so_far:
                if entity['type'] == 'politician':
                    # grab some additional metadata
                    top_sectors = api.pol_industries(entity['id'], cycle='-1')
                    
                    sectors_barchart_data = []
                    for record in top_sectors:
                        sectors_barchart_data.append({
                            'key': generate_label(standardize_organization_name(record['industry']), max_length=30),
                            'value' : record['amount'],
                        })
                        pg_entity['sectors_barchart_data'] = json.dumps(sectors_barchart_data[:5])
                
                elif entity['type'] == 'organization':
                    party_breakdown = api.org_party_breakdown(entity['id'], cycle='-1')
                    for key, values in party_breakdown.iteritems():
                        party_breakdown[key] = float(values[1])
                    if len(party_breakdown.keys()) < 2:
                        continue
                    pg_entity['party_breakdown'] = json.dumps(pie_validate(party_breakdown))
                
                seen_so_far.append(entity['id'])
        
        out = [entry]
        print out
        return out

register_region(Stories)

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