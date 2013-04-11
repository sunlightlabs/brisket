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

from entity_views import *
from entity_landing_views import *
from dataset_landing_views import *

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
        kwargs = {}
        query = submitted_form.cleaned_data['query'].strip()
        cycle = request.GET.get('cycle', DEFAULT_CYCLE)

        # see ticket #545
        query = query.replace(u"’", "'")

        query = unicodedata.normalize('NFKD',query).encode('ascii','ignore')

        # if a user submitted the search value from the form, then
        # treat the hyphens as intentional. if it was from a url, then
        # the name has probably been slug-ized and we need to remove
        # any single occurences of hyphens.
        if not request.GET.get('from_form', None):
            query = query.replace('-', ' ')

        results = api.entities.search(query)

        # limit the results to only those entities with an ID.
        entity_results = [result for result in results if result['id']]

        # if there's just one results, redirect to that entity's page
        if len(entity_results) == 1:
            result_type = entity_results[0]['type']
            name = slugify(entity_results[0]['name'])
            _id = entity_results[0]['id']
            return HttpResponseRedirect('/%s/%s/%s%s' % (result_type, name, _id, "?cycle=" + cycle if cycle != "-1" else ""))

        kwargs['query'] = query
        kwargs['contributor_search_link'] = _get_td_url('individual', query, None, None)

        if len(entity_results) == 0:
            kwargs['sorted_results'] = None
        else:
            # sort the results by type
            sorted_results = {'organization': [], 'politician': [], 'individual': [], 'lobbying_firm': [], 'industry': [], 'superpac': []}
            for result in entity_results:
                if result['type'] == 'organization' and result['lobbying_firm'] == True:
                    sorted_results['lobbying_firm'].append(result)
                elif result['type'] == 'organization' and result['is_superpac'] == True:
                    sorted_results['superpac'].append(result)
                else:
                    sorted_results[result['type']].append(result)

            # sort each type by amount
            sorted_results['industry']      = sorted(sorted_results['industry'],      key=lambda x: float(x['total_given']), reverse=True)
            sorted_results['organization']  = sorted(sorted_results['organization'],  key=lambda x: float(x['total_given']), reverse=True)
            sorted_results['individual']    = sorted(sorted_results['individual'],    key=lambda x: float(x['total_given']), reverse=True)
            sorted_results['politician']    = sorted(sorted_results['politician'],    key=lambda x: float(x['total_received']), reverse=True)
            sorted_results['lobbying_firm'] = sorted(sorted_results['lobbying_firm'], key=lambda x: float(x['firm_income']), reverse=True)

            # keep track of how many there are of each type of result
            kwargs['num_industries']   = len(sorted_results['industry'])
            kwargs['num_orgs']   = len(sorted_results['organization'])
            kwargs['num_pols']   = len(sorted_results['politician'])
            kwargs['num_indivs'] = len(sorted_results['individual'])
            kwargs['num_firms']  = len(sorted_results['lobbying_firm'])
            kwargs['num_superpacs'] = len(sorted_results['superpac'])
            kwargs['cycle'] = cycle
            kwargs['sorted_results'] = sorted_results
        return render_to_response('search/results.html', kwargs, RequestContext(request))
    else:
        return HttpResponseRedirect('/')