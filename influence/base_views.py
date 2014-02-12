from collections import OrderedDict

from django.http import Http404
from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from influence.forms import ElectionCycle
from influence.helpers import get_metadata, get_summaries, standardize_name, \
        get_source_display_name, generate_label, barchart_href
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver, \
        IndividualNameCleaver
from settings import FIRST_CYCLE, LATEST_CYCLE, DEBUG
from influenceexplorer import DEFAULT_CYCLE
import json

class MultiSectionView(View):
    sections = []
    template = 'section_base/multisection_base.html'

    def prepare_context(self, request):
        return {'sections': OrderedDict()}

    def get(self, request):
        context = self.prepare_context(request)

        suppress_cache = False
        for section in self.sections:
            s = section(self)
            s.build_section()
            context['sections'][section.label] = s

            if s.failed or s.suppress_cache:
                suppress_cache = True

        response = render_to_response(self.template, context, self.build_request_context(request))

        if suppress_cache:
            response['Cache-Control'] = "max-age=0"

        return response

    def build_request_context(self, request):
        context_variables = {}

        params = request.GET.copy()
        params['cycle'] = self.cycle

        available_cycles = [str(x) for x in range(int(FIRST_CYCLE), int(LATEST_CYCLE) + 1, 2)]
        available_cycles.append("-1")

        context_variables['cycle_form'] = ElectionCycle(available_cycles, params)

        return RequestContext(request, context_variables)

class EntityView(MultiSectionView):
    type = None

    @property
    def template(self):
        return 'entities/%s.html' % self.type

    def check_metadata(self):
        try:
            icycle = int(self.cycle)
        except:
            raise Http404
        if not self.metadata['entity_info']['years']:
            raise Http404
        elif icycle != -1 and (icycle < int(self.metadata['entity_info']['years']['start']) or icycle > int(self.metadata['entity_info']['years']['end'])):
            raise Http404
        elif icycle > LATEST_CYCLE:
            raise Http404
        elif self.metadata['entity_info']['type'] != self.type:
            raise Http404

    def prepare_context(self, request):
        try:
            self.metadata, self.cycle = get_metadata(self.entity_id, request, self.type)
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                raise Http404
            raise

        self.check_metadata()

        self.standardized_name = standardize_name(self.metadata['entity_info']['name'], self.type)
        self.external_ids = self.metadata['entity_info']['external_ids']

        context = super(EntityView, self).prepare_context(request)
        context['entity_id'] = self.entity_id
        context['cycle'] = self.cycle
        context['entity_info'] = self.metadata['entity_info']
        context['entity_info']['metadata']['source_display_name'] = get_source_display_name(self.metadata['entity_info']['metadata'])

        if self.cycle != DEFAULT_CYCLE and unicode(str(self.cycle)) in self.metadata['entity_info']['metadata']:
            # copy the current cycle's metadata into the generic metadata spot
            self.metadata['entity_info']['metadata'].update(self.metadata['entity_info']['metadata'][unicode(str(self.cycle))])

        return context

    def get(self, request, entity_id):
        self.entity_id = entity_id

        return super(EntityView, self).get(request)

class EntityLandingView(MultiSectionView):
    label = None

    @property
    def template(self):
        return 'entity_landing/%s_landing.html' % self.label

    def check_summaries(self):
        pass

    def prepare_context(self, request):
        try:
            self.summaries, self.cycle = get_summaries(self.label, request)
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                raise Http404
            raise

        self.check_summaries()

        context = super(EntityLandingView, self).prepare_context(request)
        context['cycle'] = self.cycle
        context['name'] = self.name
        context['label'] = self.label
        context['summaries'] = self.summaries

        return context

    def get(self, request):

        return super(EntityLandingView, self).get(request)

class Section(object):
    template = None
    error_template = "section_base/section_error.html"
    external_links_template = "section_base/external_links.html"
    enabled = True
    failed = False
    suppress_cache = False
    data = {}

    label = None
    name = None

    def __init__(self, entity_view):
        self.entity = entity_view

    def should_fetch(self):
        return True

    def fetch(self):
        return True

    def build_section_data(self):
        return True

    def build_section(self):
        if self.enabled:
            self.enabled = self.should_fetch()

        if self.enabled:
            try:
                self.enabled = self.fetch()
            except:
                if DEBUG:
                    raise
                self.failed = True
                return

        if self.enabled:
            try:
                self.build_section_data()
            except:
                if DEBUG:
                    raise
                self.failed = True
                return

class EntityLandingSection(Section):

    def __init__(self, entity_view):
        super(EntityLandingSection, self).__init__(entity_view)
        self.select_cleaver()

    def select_cleaver(self):
        if self.entity.label in ['individual','lobbyist']:
            self.entity_type = 'individual'
            self.cleaver = IndividualNameCleaver
        elif self.entity.label == 'pol':
            self.entity_type = 'politician'
            self.cleaver = PoliticianNameCleaver
        else:
            if self.entity.label == 'industry':
                self.entity_type = 'industry'
            else:
                self.entity_type = 'organization'
            self.cleaver = OrganizationNameCleaver

    def should_fetch(self):
        return bool(self.entity.summaries[self.label])

    def fetch(self):
        self.data = self.entity.summaries[self.label]
        return True

    def prepare_parent_child_tree(self,indicator):
        obj = self.data[indicator]
        for parent in obj:
            for child in parent['children']:
                child_name = self.cleaver(child['name']).parse()
                child_name.honorific = None
                child['name'] = generate_label(str(child_name))
                child['href'] = barchart_href(child,self.entity.cycle,self.entity_type)
        return json.dumps(obj)
