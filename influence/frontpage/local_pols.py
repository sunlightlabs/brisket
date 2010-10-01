from influence.frontpage.region import Region
from influence.frontpage import register_region

class LocalPols(Region):
    name = 'local_pols'

register_region(LocalPols)
