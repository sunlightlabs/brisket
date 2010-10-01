from django.core.management.base import BaseCommand, CommandError
from influence.frontpage import regions

class Command(BaseCommand):
    help = 'Generates and statically caches versions of regions to go on the home page.'
    
    def handle(self, *args, **options):
        if args:
            regs = dict(filter(lambda s: s[0] in args, regions.items())).values()
        else:
            regs = regions.values()
                
        for region in regs:
            reg = region()
            print 'Generating %s...' % reg.name
            reg.render_to_file()
