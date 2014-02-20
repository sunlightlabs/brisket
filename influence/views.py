# coding=utf-8

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import pluralize, slugify
from django.utils.datastructures import SortedDict
from django_localflavor_us.us_states import US_STATES, US_TERRITORIES
from feedinator.models import Feed
from influence import external_sites
from influence.forms import SearchForm, ElectionCycle
from influence.helpers import generate_label, barchart_href, \
    bar_validate, pie_validate, get_data_types, DummyEntity, \
    filter_bad_spending_descriptions, make_bill_link, get_top_pages, \
    standardize_name
from influenceexplorer import DEFAULT_CYCLE
from influence.external_sites import _get_td_url
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver
from name_cleaver.names import PoliticianName
from settings import LATEST_CYCLE, TOP_LISTS_CYCLE, DOCKETWRENCH_URL, INSTALLED_APPS, api
from urllib2 import URLError, HTTPError
from collections import defaultdict, OrderedDict
from influence.cache import cache
import datetime
import json
import unicodedata
import operator
import urllib

from entity_views import *
from entity_landing_views import *
from dataset_landing_views import *
from place_landing_views import *

from BeautifulSoup import BeautifulSoup

# Exceptions need a functioning unicode method
# for Sentry. URLError and its subclass HTTPError
# do not. So monkey patching.
URLError.__unicode__ = lambda self: unicode(self.__str__())


def handle_errors(f):
    def wrapped_f(*args, **params):
        try:
            return f(*args, **params)
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                raise Http404
            raise

    return wrapped_f


def brisket_context(request):
    return RequestContext(request, {'search_form': SearchForm()})


def entity_context(request, cycle, available_cycles):
    context_variables = {}

    params = request.GET.copy()
    params['cycle'] = cycle

    context_variables['cycle_form'] = ElectionCycle(available_cycles, params)

    return RequestContext(request, context_variables)


def entity_redirect(request, entity_id):
    entity = api.entities.metadata(entity_id)

    name = slugify(entity['name'])

    return redirect('{}_entity'.format(entity['type']), entity_id=entity_id)

def entity_preview_redirect(request, entity_id, type=None):
    entity = api.entities.metadata(entity_id)

    name = slugify(entity['name'])

    return redirect('entity_preview', entity_id=entity_id, type=entity['type'])


def entity_preview(request, entity_id, type):

    if type == 'politician':
        cycle, standardized_name, metadata, context = prepare_entity_view(request, entity_id, type)
        return render_to_response('{}_preview.html'.format(type), context,
                              entity_context(request, cycle, metadata['available_cycles']))
    else:
        return entity_redirect(request, entity_id)

#this is the index
def index(request):
    #ID of the feed is hardcoded as feed 1 since it's the only feed we're using right now. This may change!
    feed = Feed.objects.get(pk=1)
    entry = feed.entries.values().latest('date_published')
    entry['title'] = entry['title'].replace('Influence Explored: ', '')
    parsed_summary = BeautifulSoup(entry['summary'])
    for e in parsed_summary.findAll('figure'):
        e.clear()
    entry['summary'] = unicode(parsed_summary)
    return render_to_response('index.html', {"feed": feed, "entry": entry, "top_pages": get_top_pages()}, brisket_context(request))

POL_STATES = STATE_CHOICES = tuple(sorted(US_STATES + US_TERRITORIES, key=lambda obj: obj[1]))

_cached_search = cache(seconds=900)(api.entities.adv_search)

def search(request, search_type, search_subtype):
    if not request.GET.get('query', None):
        HttpResponseRedirect('/')

    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():
        query = submitted_form.cleaned_data['query'].strip()

        # see ticket #545
        query = query.replace(u"’", "'")

        query = unicodedata.normalize('NFKD',query).encode('ascii','ignore')

        # if a user submitted the search value from the form, then
        # treat the hyphens as intentional. if it was from a url, then
        # the name has probably been slug-ized and we need to remove
        # any single occurences of hyphens.
        if not request.GET.get('from_form', None):
            query = query.replace('-', ' ')

        per_page = 5 if search_type == 'all' else 10
        page = 1 if search_type == 'all' else request.GET.get('page', 1)

        results = {'per_page_slice': ":%s" % per_page}

        search_kwargs = defaultdict(dict)
        if search_subtype:
            search_kwargs[search_type]['subtype'] = search_subtype
            if search_subtype == 'politicians':
                state = request.GET.get('state', None)
                seat = request.GET.get('seat', None)
                party = request.GET.get('party', None)

                if state:
                    results['state_filter'] = state
                    search_kwargs[search_type]['state'] = state
                if seat:
                    results['seat_filter'] = seat
                    search_kwargs[search_type]['seat'] = seat
                if party:
                    results['party_filter'] = party
                    search_kwargs[search_type]['party'] = party

        results['result_sets'] = OrderedDict([
            ('groups', _cached_search(query, per_page=10, page=page, type=('organization', 'industry'), **(search_kwargs['groups']))),
            ('people', _cached_search(query, per_page=10, page=page, type=('individual', 'politician'), **(search_kwargs['people'])))
        ])

        all_results = reduce(operator.add, [t['results'] for t in results['result_sets'].values()])

        if len(all_results) == 1:
            # if there's just one result, redirect to that entity's page
            result_type = all_results[0]['type']
            name = slugify(standardize_name(all_results[0]['name'], result_type))
            _id = all_results[0]['id']
            return HttpResponseRedirect('/%s/%s/%s' % (result_type, name, _id))
        elif len(all_results) > 0 and search_type == "all":
            # if there's only one type of result, redirect to a sub-search
            for result_type, result_set in results['result_sets'].items():
                if len(result_set['results']) == len(all_results):
                    return HttpResponseRedirect('/search/%s?%s' % (result_type, urllib.urlencode(request.GET)))


        # do a tiny bit of regulations-specific hackery: if there are org results, stash a thread-local copy of the Docket Wrench entity list so it doesn't have to be recreated for each result
        dw_entity_list = None
        if results['result_sets']['groups']['results']:
            external_sites._dw_local.dw_entity_list = dw_entity_list = external_sites.get_docketwrench_entity_list()

        for result in (all_results if search_type == 'all' else results['result_sets'][search_type]['results']):
            result['url'] = "/%s/%s/%s" % (result['type'], slugify(standardize_name(result['name'], result['type'])), result['id'])

            if result['type'] == 'organization':
                result['has_fec_id'] = len([eid for eid in result['external_ids'] if eid['namespace'] == "urn:fec:committee"]) > 0

            # munge results a bit to handle available sections
            result.update(get_data_types(result['type'], result['totals']))
            result['sections'] = []
            # simulate an entity view so we can query said entity view's sections to see if they're availble
            dummy_view = DummyEntity(result)

            view_type = entity_views[result['type']]
            for section_type in view_type.sections:
                dummy_section = section_type(dummy_view)
                if dummy_section.should_fetch():
                    result['sections'].append(dummy_section)

        # clean up after DW hackery
        if dw_entity_list:
            del external_sites._dw_local.dw_entity_list

        results['total_results'] = sum([result.get('total', 0) for result in results['result_sets'].values()])
        results['has_results'] = (results['total_results'] if search_type == 'all' else results['result_sets'][search_type]['total']) > 0
        results['query'] = query
        results['search_type'] = search_type
        results['total'] = len(all_results)

        results['search_subtype'] = search_subtype
        results['search_subtypes'] = {
            'people': [('all', 'All people'), ('contributors', 'Contributors'), ('lobbyists', 'Lobbyists'), ('politicians', 'Politicians')],
            'groups': [('all', 'All groups'), ('industries', 'Industries'), ('lobbying_firms', 'Lobbying organizations'), ('political_groups', 'Political groups'), ('other_orgs', 'Businesses and other organizations')]
        }

        qs_attrs = request.GET.copy()
        if 'page' in qs_attrs:
            del qs_attrs['page']
        results['qs'] = urllib.urlencode(qs_attrs)

        if search_subtype == 'politicians':
            results['states'] = POL_STATES
            results['seats'] = ["federal:president", "federal:senate", "federal:house", "state:governor", "state:judicial", "state:lower", "state:upper", "state:office"]
            results['parties'] = [('D', 'Democrat'), ('R', 'Republican'), ('O', 'Other')]
        
        return render_to_response('search/results.html', results, RequestContext(request))
    else:
        return HttpResponseRedirect('/')
