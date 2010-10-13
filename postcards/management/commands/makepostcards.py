from django.core.management import BaseCommand
from optparse import make_option
import os, sys
import postcards
from influence import api
from django.conf import settings
from django.template.loader import render_to_string
from gevent.pool import Pool
from gevent import monkey
import gevent
from django.utils.datastructures import SortedDict
from influence.helpers import standardize_organization_name, standardize_industry_name

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--photos_only',
            action='store_true',
            dest='photos_only',
            default=False,
        ),
        make_option('--svg-only',
            action='store_true',
            dest='svg_only',
            default=False,
        ),
        make_option('--rasterize-only',
            action='store_true',
            dest='rasterize_only',
            default=False,
        ),
        make_option('--district',
            action='store',
            dest='district',
            default=None,
        )
    )
    
    def handle(self, *args, **options):
        self.svg = True
        self.raster = True
        if options['svg_only']:
            self.raster = False
        if options['rasterize_only']:
            self.svg = False
        
        # get ready for gevent
        monkey.patch_all()
        
        self.postcard_dir = os.path.dirname(postcards.__file__)
        self.static_dir = os.path.join(self.postcard_dir, 'static')
        self.svg_dir = os.path.join(self.postcard_dir, 'static', 'svg')
        self.pdf_dir = os.path.join(self.postcard_dir, 'static', 'pdf')
        self.png_dir = os.path.join(self.postcard_dir, 'static', 'png')
        
        for dir in [self.static_dir, self.svg_dir, self.pdf_dir, self.png_dir]:
            if not os.path.exists(dir):
                os.mkdir(dir)
        
        if self.svg:
            sys.stdout.write('Fetching districts...\n')
            congress = {'federal:house': {}, 'federal:senate': {}}
            if options['district']:
                self.districts = [options['district']]
            else:
                self.districts = self.get_districts()
            
            def get_district(district):
                state = district.split('-')[0]
                sys.stdout.write('Fetching candidates for %s...\n' % district)
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
                                pass
                        
                        # grab these candidates' metadata
                        for candidate in selected:
                            sys.stdout.write('Fetching metadata for %s...\n' % candidate['name'])
                            candidate['entity_info'] = api.entity_metadata(candidate['entity_id'], cycle=settings.LATEST_CYCLE)
                            candidate['contributions'] = api.pol_contributors(candidate['entity_id'], cycle=settings.LATEST_CYCLE)
                            candidate['industries'] = api.pol_industries(candidate['entity_id'], cycle=settings.LATEST_CYCLE)
                            if str(settings.LATEST_CYCLE) in candidate['entity_info']['totals']:
                                candidate['total'] = candidate['entity_info']['totals'][str(settings.LATEST_CYCLE)]['recipient_amount']
                            else:
                                candidate['total'] = 0
                        
                        # store the candidates for later use
                        congress[chamber][key] = selected
            
            # fire up gevent to fetch them all
            pool = Pool(10)
            for district in self.districts:
                pool.spawn(get_district, district)
            pool.join()
            
            sys.stdout.write('Generating SVGs...\n')
            for chamber in congress.keys():
                for loc in congress[chamber].keys():
                    # single-candidate cards
                    for candidate in congress[chamber][loc]:
                        sys.stdout.write('Generating SVG for %s...\n' % candidate['name'])
                        
                        # contribution data
                        contributions = SortedDict()
                        for cont in candidate['contributions'][:5]:
                            contributions[standardize_organization_name(cont['name'])] = cont['total_amount']
                        
                        # industry data
                        industries = SortedDict()
                        for cont in candidate['industries'][:5]:
                            industries[standardize_industry_name(cont['industry'])] = cont['amount']
                        
                        svg_static = os.path.join(self.svg_dir, 'candidate_%s.svg' % candidate['entity_id'])
                        
                        out = render_to_string('postcards/single_card.svg', {
                            'entity_info': candidate['entity_info'],
                            'contributions': contributions,
                            'industries': industries,
                            'district_info': candidate,
                            'total': int(round(float(candidate['total']))),
                        })
                        f = open(svg_static, 'wb')
                        f.write(out.encode('utf-8'))
                        f.close()
    
    def get_districts(self):
        # temporary until we have a real API for it
        f = open(os.path.join(self.postcard_dir, 'districts.dat'))
        out = f.read().split('\n')
        f.close()
        return out