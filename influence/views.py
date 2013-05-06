# coding=utf-8

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import pluralize, slugify
from django.utils.datastructures import SortedDict
from feedinator.models import Feed
from influence import external_sites
from influence.forms import SearchForm, ElectionCycle
from influence.helpers import generate_label, barchart_href, \
    bar_validate, pie_validate, \
    filter_bad_spending_descriptions, make_bill_link, get_top_pages
from influenceexplorer import DEFAULT_CYCLE
from influence.external_sites import _get_td_url
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver
from name_cleaver.names import PoliticianName
from settings import LATEST_CYCLE, TOP_LISTS_CYCLE, DOCKETWRENCH_URL, api
from urllib2 import URLError, HTTPError
import datetime
import json
import unicodedata
import operator

from entity_views import *
from entity_landing_views import *
from dataset_landing_views import *
from place_landing_views import *

#this is the index
def index(request):
    #ID of the feed is hardcoded as feed 1 since it's the only feed we're using right now. This may change!
    feed = Feed.objects.get(pk=1)
    entry = feed.entries.values().latest('date_published')
    entry['title'] = entry['title'].replace('Influence Explored: ', '')
    return render_to_response('index.html', {"feed": feed, "entry": entry, "top_pages": get_top_pages()}, RequestContext(request))


def search(request):
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

        results = {
            'people': api.entities.adv_search(query, type=('individual', 'politician'), per_page=5),
            'groups': api.entities.adv_search(query, type=('organization', 'industry'), per_page=5)
        }

        all_results = reduce(operator.add, [t['results'] for t in results.values()])

        # if there's just one results, redirect to that entity's page
        if len(all_results) == 1:
            result_type = all_results[0]['type']
            # FIXME: cleave first
            name = slugify(all_results[0]['name'])
            _id = all_results[0]['id']
            return HttpResponseRedirect('/%s/%s/%s' % (result_type, name, _id))

        results['has_results'] = results['people']['total'] + results['groups']['total'] > 0
        results['query'] = query
        
        return render_to_response('search/results.html', results, RequestContext(request))
    else:
        return HttpResponseRedirect('/')