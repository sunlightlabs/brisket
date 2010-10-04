from influence.frontpage.region import Region
from influence.frontpage import register_region
from django.conf import settings
from django.template.loader import render_to_string
import urlparse
from datetime import datetime, timedelta
from influence import api
from influence.models import PageRequest
from django.db.models import Q, Count
from util import single_map

class TopPages(Region):
    name = 'top_pages'
    
    def get_context(self):
        # grab significant entities
        page_views = PageRequest.objects.filter(Q(path__startswith='/organization/') | Q(path__startswith='/politician/') | Q(path__startswith='/individual/'), requested_at__gte=datetime.now() - timedelta(days=3))
        
        counts = {}
        for view in page_views:
            id = view.path.split('/')[-1]
            if id in counts:
                counts[id] += 1
            else:
                counts[id] = 1
        
        sorted_counts = sorted(counts.items(), cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)[:10]
        
        max_count = max([c[1] for c in sorted_counts])
        
        ranking = []
        for c in sorted_counts:
            ranking.append({
                'id': c[0],
                'count': c[1],
                'metadata': api.entity_metadata(c[0]),
                'percentage': int(round(single_map(c[1], 0, max_count, 0, 100))),
            })
        
        
        
        return {'top_pages': ranking}

register_region(TopPages)
