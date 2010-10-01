regions = {}

def register_region(region):
    if region.name not in regions:
        regions[region.name] = region

from influence.frontpage import top_news
from influence.frontpage import local_pols
#from influence.frontpage import stories
from influence.frontpage import top_pages