from influence.frontpage.region import Region
from influence.frontpage import register_region
from django.conf import settings
import feedparser, re
import urllib
from influence import api
from util import catcodes
from influence.helpers import generate_label, pie_validate
import json
import sys, datetime, time

class TopNews(Region):    
    name = 'top_news'
    
    def get_context(self):
        #grab Yahoo politics feed
        feed = feedparser.parse("http://rss.news.yahoo.com/rss/politics")
        
        pg_entries = []
        for entry in feed['entries'][:5]:
            pg_entry = {
                'title': entry['title'].replace('(%s)' % entry['source']['title'], '').strip(),
                'photo': entry['media_content'][0]['url'] if 'media_content' in entry else '',
                'link': entry['link'],
                'source': entry['source']['title'],
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
            
        for entry in pg_entries:
            entry['entities'] = sorted(filter(lambda s: s['tdata_id'] is not None, entry['pg_struct']['entities']), cmp=lambda a, b: cmp(a['relevance'], b['relevance']), reverse=True)
            entry['text'] = entry['pg_struct']['source_content'].split('</p>')[1] + '</p>'
        
        entries = filter(lambda a: len(a['entities']) > 0, pg_entries)
        
        return {'entries': entries[:5]}

register_region(TopNews)