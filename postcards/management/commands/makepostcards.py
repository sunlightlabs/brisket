from django.core.management import BaseCommand
from optparse import make_option
import os, sys
import postcards
from settings import api
from django.conf import settings
from django.template.loader import render_to_string
from gevent.pool import Pool
from gevent import monkey
import gevent
from django.utils.datastructures import SortedDict
from influence.helpers import standardize_organization_name, standardize_industry_name
from name_cleaver import PoliticianNameCleaver
from django.template.defaultfilters import slugify
import urllib2
import re
import subprocess

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--photos-only',
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
        self.photos = True
        if options['svg_only']:
            self.raster = False
            self.photos = False
        if options['rasterize_only']:
            self.svg = False
            self.photos = False
        if options['photos_only']:
            self.svg = False
            self.raster = False
        
        # get ready for gevent
        monkey.patch_all()
        
        self.postcard_dir = os.path.dirname(postcards.__file__)
        self.static_dir = os.path.join(self.postcard_dir, 'static')
        self.svg_dir = os.path.join(self.postcard_dir, 'static', 'svg')
        self.pdf_dir = os.path.join(self.postcard_dir, 'static', 'pdf')
        self.photo_dir = os.path.join(self.svg_dir, 'resources', 'photos')
        self.png_dir = os.path.join(self.postcard_dir, 'static', 'png')
        
        for dir in [self.static_dir, self.svg_dir, self.pdf_dir, self.png_dir, self.photo_dir]:
            if not os.path.exists(dir):
                os.mkdir(dir)
        
        self.districts = None
        if self.svg or self.photos or options['district']:
            sys.stdout.write('Fetching districts...\n')
            congress = {'federal:house': {}, 'federal:senate': {}}
            if options['district']:
                self.districts = [options['district']]
            else:
                self.districts = self.get_districts()
            
            def get_district(district):
                state = district.split('-')[0]
                sys.stdout.write('Fetching candidates for %s...\n' % district)
                candidates = api.entities.candidates_by_location(district)
                
                for chamber in congress.keys():
                    key = district if chamber == 'federal:house' else state
                    if key not in congress[chamber]:
                        members = filter(lambda s: s['seat'] == chamber, candidates)
                        selected = []
                        for party in ['D', 'R']:
                            try:
                                candidate = sorted(filter(lambda s: s['party'] == party, members), cmp=lambda a, b: cmp(a['name'], b['name'])).pop(0)
                                selected.append(candidate)
                            except:
                                pass
                        
                        # grab these candidates' metadata
                        if self.svg:
                            for candidate in selected:
                                sys.stdout.write('Fetching metadata for %s...\n' % candidate['name'])
                                candidate['entity_info'] = api.entities.metadata(candidate['entity_id'], cycle=settings.LATEST_CYCLE)
                                candidate['contributions'] = api.pol.contributors(candidate['entity_id'], cycle=settings.LATEST_CYCLE)
                                candidate['industries'] = api.pol.industries(candidate['entity_id'], cycle=settings.LATEST_CYCLE)
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
            
            if self.photos:
                photos = os.listdir(self.photo_dir)
                
                def fetch_photos(candidate):
                    votesmart_id = candidate['votesmart_id']
                    
                    # first try large, then small
                    for ext in ['_lg.jpg', '.jpg']:
                        filename = '%s%s' % (votesmart_id, ext)
                        if os.path.exists(os.path.join(self.photo_dir, filename)):
                            #sys.stdout.write('Already have photo %s for candidate %s\n' % (filename, candidate['name']))
                            return
                        try:
                            url = 'http://votesmart.org/canphoto/%s' % filename
                            u=urllib2.urlopen(url)
                            f = open(os.path.join(self.photo_dir, filename), 'wb')
                            f.write(u.read())
                            sys.stdout.write('Found photo %s for candidate %s\n' % (filename, candidate['name']))
                            return
                        except:
                            pass
                    sys.stdout.write("No photo found for candidate %s\n" % candidate['name'])
                
                # fetch photos
                sys.stdout.write('Fetching photos...\n')
                for chamber in congress.keys():
                    for loc in congress[chamber].keys():
                        for candidate in congress[chamber][loc]:
                            pool.spawn(fetch_photos, candidate)
                pool.join()
            
            if self.svg:
                sys.stdout.write('Generating SVGs...\n')
                # build up a list of photos
                separator = re.compile(r'[\._]')
                photos = os.listdir(self.photo_dir)
                pics = dict([[int(separator.split(photo)[0]), photo] for photo in photos])
                
                # generate SVGs
                for chamber in congress.keys():
                    for loc in congress[chamber].keys():
                        if chamber == 'federal:senate':
                                district_name = loc.split('-')[0]
                        else:
                            district_name = loc
                        chamber_name = chamber.split(':')[-1]
                        
                        pair = []
                        # single-candidate cards
                        for candidate in congress[chamber][loc]:
                            sys.stdout.write('Generating SVG for %s candidate %s...\n' % (chamber_name.capitalize(), candidate['name']))
                            
                            # contribution data
                            contributions = SortedDict()
                            for cont in candidate['contributions'][:5]:
                                if float(cont['total_amount']) >= 0:
                                    contributions[standardize_organization_name(cont['name'])] = cont['total_amount']
                            
                            # industry data
                            industries = SortedDict()
                            for cont in candidate['industries'][:5]:
                                if float(cont['amount']) >= 0:
                                    industries[standardize_industry_name(cont['name'])] = cont['amount']
                            
                            #deal with the name
                            name_obj = PoliticianNameCleaver(candidate['name']).parse()
                            candidate['standard_name'] = str(name_obj)
                            candidate['first_name'] = name_obj.first
                            candidate['last_name'] = name_obj.last
                            candidate['suffix'] = name_obj.suffix
                            
                            if len(candidate['standard_name']) > 24:
                                candidate['standard_name'] = '%s %s %s' % (candidate['first_name'], candidate['last_name'], candidate['suffix']) if candidate['suffix'] else '%s %s' % (candidate['first_name'], candidate['last_name'])
                            svg_static = os.path.join(self.svg_dir, 'candidate_%s_%s.svg' % (slugify(candidate['last_name']), candidate['entity_id']))
                            
                            card_context = {
                                'entity_info': candidate['entity_info'],
                                'contributions': contributions,
                                'industries': industries,
                                'district_info': candidate,
                                'total': int(round(float(candidate['total']))),
                                'photo': pics[candidate['votesmart_id']] if candidate['votesmart_id'] in pics else None,
                            }
                            
                            out = render_to_string('postcards/single_card.svg', card_context)
                            f = open(svg_static, 'wb')
                            f.write(out.encode('utf-8'))
                            f.close()
                            
                            pair.append(card_context)
                        
                        # double-candidate card
                        if len(congress[chamber][loc]) > 1:
                            pair.sort(cmp=cmp_candidates)
                            
                            sys.stdout.write('Generating SVG for %s race %s...\n' % (chamber_name.capitalize(), district_name))
                            pair_svg_static = os.path.join(self.svg_dir, 'race_%s_%s.svg' % (chamber_name, district_name))
                            
                            out = render_to_string('postcards/pair_card.svg', {'candidates': pair})
                            f = open(pair_svg_static, 'wb')
                            f.write(out.encode('utf-8'))
                            f.close()
                        else:
                            sys.stdout.write('No second candidate for %s race %s; skipping card.\n' % (chamber_name.capitalize(), district_name))
            
        if self.raster:
            batik_path = getattr(settings, 'BATIK_RASTERIZER_PATH', None)
            if not batik_path:
                sys.stdout.write('Setting BATIK_RASTERIZER_PATH not found.\n')
                return
            
            if self.districts:
                # we're generating specific candidate PDFs, so all the data should be there
                to_render = []
                for chamber in congress.keys():
                    for loc in congress[chamber].keys():
                        # single-candidate cards
                        for candidate in congress[chamber][loc]:
                            svg_static = os.path.join(self.svg_dir, 'candidate_%s_%s.svg' % (slugify(candidate['last_name']), candidate['entity_id']))
                            to_render.append(svg_static)
                            
                            if chamber == 'federal:senate':
                                district_name = loc.split('-')[0]
                            else:
                                district_name = loc
                            pair_svg_static = os.path.join(self.svg_dir, 'race_%s_%s.svg' % (chamber.split(':')[-1], district_name))
                            if pair_svg_static not in to_render and os.path.exists(pair_svg_static):
                                to_render.append(pair_svg_static)
            else:
                svgs = filter(lambda s: s.startswith('candidate') or s.startswith('race'), os.listdir(self.svg_dir))
                to_render = [os.path.join(self.svg_dir, s) for s in svgs]
            
            args = ['java', '-jar', batik_path, '-d', self.pdf_dir]
            args.extend(to_render)
            
            # PDF run
            pdf_args = args + ['-m', 'application/pdf']
            sys.stdout.write('Generating PDFs...\n')
            batik = subprocess.Popen(pdf_args, stdout=sys.stdout)
            batik.wait()
    
    def get_districts(self):
        return [item['district'] for item in api.entities.election_districts()]

def cmp_candidates(a, b):
    status_cmp = -1 * cmp(a['district_info']['seat_status'], b['district_info']['seat_status'])
    if status_cmp:
        return status_cmp
    else:
        return cmp(a['district_info']['last_name'], b['district_info']['last_name'])
