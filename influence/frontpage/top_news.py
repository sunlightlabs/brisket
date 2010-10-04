from influence.frontpage.region import Region
from influence.frontpage import register_region
from django.conf import settings
import feedparser, re
import urllib
from influence import api
from util import catcodes
from influence.helpers import generate_label, pie_validate
from util import multi_list_map
import json
import sys, datetime, time

class TopNews(Region):    
    name = 'top_news'
    url = 'http://rss.news.yahoo.com/rss/politics'
    to_parse = 10
    to_return = 5
    
    def get_context(self):
        #grab Yahoo politics feed
        feed = feedparser.parse(self.url)
        
        pg_entries = []
        for entry in feed['entries'][:self.to_parse]:
            source = entry['source']['title'] if 'source' in entry else ''
            pg_entry = {
                'title': entry['title'].replace('(%s)' % source, '').strip(),
                'photo': entry['media_content'][0]['url'] if 'media_content' in entry else '',
                'link': entry['link'],
                'source': source,
                'date': datetime.datetime(*entry['date_parsed'][:6]),
                'pg_struct': None,
            }
            
            # make initial request to poligraft
            pg_url = 'http://poligraft.com/poligraft?url=%s&json=1' % urllib.quote(pg_entry['link'])
            sys.stdout.write('Loading %s...\n' % pg_url)
            pg_data = json.loads(urllib.urlopen(pg_url).read())
            pg_entry['pg_id'] = pg_data['slug']
            pg_entry['pg_url'] = 'http://poligraft.com/%s' % pg_data['slug']
            
            pg_entries.append(pg_entry)
        
        # now make more requests until the processing is done on all of them
        while True:
            all_processed = True
            for entry in pg_entries:
                if not entry['pg_struct']:
                    url = '%s.json' % entry['pg_url']
                    sys.stdout.write('Loading %s...\n' % url)
                    data = json.loads(urllib.urlopen(url).read())
                    if data['processed']:
                        entry['pg_struct'] = data
                all_processed = all_processed and bool(entry['pg_struct'])
            if all_processed:
                break
            else:
                time.sleep(1)
        
        entries = self.process_entries(pg_entries)
        
        return {'entries': entries[:self.to_return]}
    
    def process_entries(self, pg_entries):
        for entry in pg_entries:
            # filter out entities not in TD, and filter out Yahoo
            entry['entities'] = sorted(filter(lambda s: s['tdata_id'] is not None and s['tdata_slug'] != 'yahoo-inc', entry['pg_struct']['entities']), cmp=lambda a, b: cmp(a['relevance'], b['relevance']), reverse=True)
            entry['text'] = entry['pg_struct']['source_content'].split('</p>')[1] + '</p>'
        
        # filter out the ones with no entities, and favor entries with photos
        entries = sorted(filter(lambda a: len(a['entities']) > 0, pg_entries), cmp=lambda a, b: cmp(bool(b['photo']), bool(a['photo'])))
        
        # add sparklines to first one
        tdata_types = {'organization': 'org', 'individual': 'indiv', 'politician': 'pol'}
        if entries:
            for entity in entries[0]['entities']:
                if entity['tdata_type'] == 'organization':
                    orig_data = json.loads(api.org_sparkline_by_party(entity['tdata_id'], cycle=settings.LATEST_CYCLE))
                    data = []
                    colors = []
                    if 'R' in orig_data:
                        data.append(orig_data['R'])
                        colors.append('e60002')
                    if 'D' in orig_data:
                        data.append(orig_data['D'])
                        colors.append('186482')
                    entity['sparkline_data'] = [[i['amount'] for i in l] for l in data]
                    colors = ['e60002', '186582']
                else:
                    data = json.loads(getattr(api, '%s_sparkline' % tdata_types[entity['tdata_type']])(entity['tdata_id'], cycle=settings.LATEST_CYCLE))
                    entity['sparkline_data'] = [[s['amount'] for s in data]]
                    colors = ['efcc01']
                entity['sparkline_url'] = sparkline(entity['sparkline_data'], colors=colors)
        
        return entries

register_region(TopNews)

def sparkline(data, size='40x20', colors=['efcc01']):
    return "http://chart.apis.google.com/chart?cht=ls&chs=%s&chdlp=r&chco=%s&chd=t:%s" % (
        size,
        ",".join(colors),
        "|".join([",".join([str(int(round(s))) for s in l]) for l in multi_list_map(data, 0, 100)]),
    )