from django.core.management import BaseCommand
from optparse import make_option
import os, sys
import postcards
from influence import api

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--svg-only',
            action='store_true',
            dest='svg_only',
            default=False,
        ),
        make_option('--rasterize-only',
            action='store_true',
            dest='rasterize_only',
            default=False,
        )
    )
    
    def handle(self, *args, **options):
        self.svg = True
        self.raster = True
        if options['svg_only']:
            self.raster = False
        if options['rasterize_only']:
            self.svg = False
        
        self.postcard_dir = os.path.dirname(postcards.__file__)
        self.svg_dir = os.path.join(self.postcard_dir, 'static', 'svg')
        self.pdf_dir = os.path.join(self.postcard_dir, 'static', 'pdf')
        self.png_dir = os.path.join(self.postcard_dir, 'static', 'png')
        
        if self.svg:
            congress = {'federal:house': {}, 'federal:senate': {}}
            self.districts = self.get_districts()
            for district in self.districts:
                state = district.split('-')[0]
                candidates = api.candidates_by_location(district)
                
                for chamber in congress.keys():
                    key = district if chamber == 'federal:house' else state
                    if key not in congress[chamber]:
                        members = filter(lambda s: s['seat'] == chamber, candidates)
                        selected = []
                        for party in ['(D)', '(R)']:
                            try:
                                candidate = sorted(filter(lambda s: s['name'].endswith(party), members), cmp=lambda a, b: cmp(a['name'], b['name'])).pop(0)
                                selected.append(candidate)
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                        congress[chamber][key] = selected
            print congress
    
    def get_districts(self):
        # temporary until we have a real API for it
        f = open(os.path.join(self.postcard_dir, 'districts.dat'))
        out = f.read().split('\n')
        f.close()
        print out
        return out