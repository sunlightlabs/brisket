from influence.frontpage.region import Region
from influence.frontpage import register_region
from django.conf import settings
from django.template.loader import render_to_string
import urlparse
from datetime import datetime, timedelta
from influence import api
from influence.models import PageRequest

class TopPages(Region):
    name = 'top_pages'
    
    def get_context(self):
        # grab significant entities
        searches = PageRequest.objects.filter(path='/search', requested_at__gte=datetime.now() - timedelta(days=3))
        counts = {}
        for search in searches:
            qs = urlparse.parse_qs(search.query_params)
            if 'query' in qs and len(qs['query']) > 0:
                term = qs['query'][0].lower()
                if term in counts:
                    counts[term] += 1
                else:
                    counts[term] = 1
        
        cloud = tagcloud(counts, 5)
        
        return {'cloud': cloud}

# altered from the version found here: http://dburke.info/blog/logarithmic-tag-clouds/
from math import log
def tagcloud(initial_counts, threshold=0, maxsize=1.75, minsize=.75):
    """usage: 
        -threshold: Tag usage less than the threshold is excluded from
            being displayed.  A value of 0 displays all tags.
        -maxsize: max desired CSS font-size in em units
        -minsize: min desired CSS font-size in em units
    Returns a list of dictionaries of the tag, its count and
    calculated font-size.
    """
    counts, taglist, tagcloud = [], [], []
    for tag in initial_counts.keys():
        if initial_counts[tag] >= threshold:
            counts.append(initial_counts[tag])
            taglist.append(tag)
    maxcount = max(counts)
    mincount = min(counts)
    constant = log(maxcount - (mincount - 1))/(maxsize - minsize or 1)
    tagcount = zip(taglist, counts)
    for tag, count in tagcount:
        size = log(count - (mincount - 1))/constant + minsize
        tagcloud.append({'tag': tag, 'count': count, 'size': round(size, 7)})
    tagcloud.sort(cmp=lambda a, b: cmp(a['tag'], b['tag']))
    return tagcloud

register_region(TopPages)
