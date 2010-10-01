from influence.frontpage.region import Region
from influence.frontpage import register_region
from django.conf import settings
import feedparser, re
from supertagging.calais import Calais
from influence import api
from util import catcodes
from influence.helpers import generate_label, pie_validate
import json

class TopNews(Region):    
    name = 'top_news'
    
    def get_context(self):
        entities = []
        font_tag = re.compile(r'<font size="-1">(.*?)</font>')
        all_tags = re.compile(r'(<.*?>|[^a-zA-Z0-9\.\'\,\-\:\? ])')
        calais = Calais(settings.CALAIS_API_KEY)
        
        #grab Google News US feed
        feed = feedparser.parse("http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=n&num=15&output=rss")
        
        for entry in feed['entries']:
            try:
                first_sentence = font_tag.findall(entry['summary_detail']['value'])[1]
                title = entry['title'].split(" - ")[0]
            
                sentence = all_tags.sub('', "%s. %s" % (title, first_sentence))
            except:
                continue
            
            try:
                result = calais.analyze(sentence)
            except:
                continue
            
            c_entities = sorted(filter(lambda s: s['_type'] in ['Person', 'Organization', 'Company'], result.entities), cmp=compare_entities, reverse=True)
            
            for entity in c_entities:
                tdata = api.entity_search(entity['name'])
                if tdata and entity['_type'] == 'Person':
                    tdata = filter(lambda s: s['type'] == 'politician' or s['type'] == 'individual', tdata)
                    tdata = sorted(tdata, cmp=lambda a, b: cmp(int(a['seat'] is not None and a['seat'].startswith('federal')), int(b['seat'] is not None and b['seat'].startswith('federal'))), reverse=True)
                elif tdata:
                    tdata = filter(lambda s: s['type'] == 'organization', tdata)
                
                if tdata:
                    entities.append(tdata[0])
                break
        
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
        
        return {'entities': out_entities[:5]}

register_region(TopNews)

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