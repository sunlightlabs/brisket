# Create your views here.

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import RequestContext
from brisket.influence.forms import SearchForm, ElectionCycle
from lib import AggregatesAPI, InfluenceNetworkBuilder
import urllib

def brisket_context(request): 
    return RequestContext(request, {'search_form': SearchForm(), 
                                    })

def entity_context(request): 
    context_variables = {}    

    if request.GET.get('query', None):
        context_variables['search_form'] = SearchForm(request.GET)
    else:
        context_variables['search_form'] = SearchForm() 
    if request.GET.get('cycle', None):
        context_variables['cycle_form'] = ElectionCycle(request.GET)
    else:
        context_variables['cycle_form'] = ElectionCycle()
    return RequestContext(request, context_variables)

def index(request):    
    return render_to_response('index.html', brisket_context(request))

def search(request):
    if not request.GET.get('query', None):
        print 'Form Error'
        HttpResponseRedirect('/')
    
    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        api = AggregatesAPI()
        results = api.entity_search(submitted_form.cleaned_data['query'])

        # limit the results to only those entities with an ID. 
        entity_results = [result for result in results if result['id']]

        sorted_results = {'organization': [], 'politician': [], 'individual': []}
        for result in entity_results:
            sorted_results[result['type']].append(result)
        print entity_results
        print sorted_results
        return render_to_response('results.html', {'sorted_results': sorted_results}, 
                                  brisket_context(request))
    else: 
        form = SearchForm(request.GET)
        return HttpResponseRedirect('/')

def organization_entity(request, entity_id):

    cycle = request.GET.get("cycle", 2010)
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    candidate_recipients = api.candidate_recipients(entity_id, cycle=cycle)

    party_breakdown = api.org_breakdown(entity_id, 'party', cycle)
    for party, values in party_breakdown.iteritems():
        party_breakdown[party] = values[1]
    piechart_party = piechart(party_breakdown, "Republicans vs. Democrats ($)")

    level_breakdown = api.org_breakdown(entity_id, 'level', cycle)
    for party, values in level_breakdown.iteritems():
        level_breakdown[party] = values[1]    
    piechart_level = piechart(level_breakdown,"State vs. Federal ($)")

    recipients_barchart = topn_barchart(candidate_recipients, 
                                        label_key='name', data_key='total_amount')

    # fake us some sparkline data
    amounts = [str(recipient['total_amount']) for recipient in candidate_recipients]
    sparkline = timeline_sparkline(amounts)
    return render_to_response('organization.html', 
                              {'entity_id': entity_id, 
                               'entity_info': entity_info,
                               'pie_chart_level' : piechart_level,
                               'pie_chart_party' : piechart_party,
                               'recipients_barchart': recipients_barchart,
                               'sparkline': sparkline,
                               },
                              entity_context(request))

def politician_entity(request, entity_id):

    #check to see if a specific election cycle was specified, using
    #2010 as default if not.
    cycle = request.GET.get("cycle", 2010)
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)

    top_contributors = api.pol_contributors(entity_id, 'org, indiv', cycle=cycle)
    top_sectors = api.top_sectors(entity_id, cycle=cycle)

    local_breakdown = api.pol_breakdown(entity_id, 'local', cycle)
    for key, values in local_breakdown.iteritems():
        local_breakdown[key] = values[1]    
    piechart_local = piechart(local_breakdown,"In State vs. Out of State ($)")

    entity_breakdown = api.pol_breakdown(entity_id, 'entity', cycle)
    for key, values in entity_breakdown.iteritems():
        entity_breakdown[key] = values[1]    
    piechart_entity = piechart(entity_breakdown,"Individuals vs. PACs ($)")

    sectors_barchart = topn_barchart(top_sectors, label_key='sector_code', 
                                     data_key='amount')

    print sectors_barchart

    # fake sparkline data
    amounts = [str(contributor['amount']) for contributor in top_contributors]
    sparkline = timeline_sparkline(amounts)
    return render_to_response('politician.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'top_contributors': top_contributors,
                               'pie_chart_instate' : piechart_local,
                               'pie_chart_source' : piechart_entity,
                               'sectors_barchart': sectors_barchart,
                               'sparkline': sparkline,
                               },
                              entity_context(request))
        
def individual_entity(request, entity_id):    
    # individuals only give contributions
    api = AggregatesAPI() 
    entity_info = api.entity_metadata(entity_id)    
    cycle = request.GET.get("cycle", 2010)

    top_recipients = api.top_recipients(entity_id, cycle=cycle)
    top_recipients_candidates = api.top_recipients(entity_id, cycle=cycle, 
                                                   entity_types='politician')
    top_recipients_pacs = api.top_recipients(entity_id, cycle=cycle, 
                                             entity_types='pac')
    candidates_barchart = topn_barchart(top_recipients_candidates, 
                                        label_key = 'name', data_key = 'amount')
    pacs_barchart = topn_barchart(top_recipients_pacs, 
                                  label_key = 'name', data_key = 'amount')    
    pie_chart_party = piechart(api.breakdown('recipients', 'party', cycle), 
                                         "Republicans vs. Democrats")
    amounts = [str(contributor['amount']) for contributor in top_recipients]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('individual.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'candidates_barchart': candidates_barchart,
                               'pacs_barchart': pacs_barchart,
                               'pie_chart_party' : pie_chart_party, 
                               'sparkline': sparkline,                               
                               },
                              entity_context(request))

def industry_detail(request, entity_id):
    cycle = request.GET.get("cycle", 2010)    
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)    
    top_industries = api.top_industries(entity_id, cycle=cycle)

    sectors = {}
    for industry in top_industries:
        industry_id = industry['category_name']        
        results = api.contributions_by_sector(entity_id, industry_id)
        sectors[industry_id] = (results)

    return render_to_response('industry_detail.html',
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'sectors': sectors,
                               },
                              entity_context(request))


def topn_barchart(data_list, label_key, data_key, n=5):
    ''' generates a horizontal bargraph of aggregate contribution data
    for the top n items in the list, where each item is a
    dict. label_key specifies the key to be used for the labels, and
    data_key for the data. '''
    if not data_list:
        return None
    max_value = max([float(item[data_key]) for item in data_list])

    # 
    data_list = data_list[0:n]

    # compile the query parameters as tuples which will be urlencoded
    # before being appended to the chart url.
    chart_type = ("cht", "bhs")
    chart_size = ("chs", "250x150")
    bar_size = ("chbh", "a")
    scaling = ("chds", "0,%f" % max_value)
    marker_axis = ("chxt", "y")
    marker_text = ("chxl", "0:|%s" % '|'.join([item[label_key] for item in data_list]))
    marker_style = ("chm", "N*cUSD*,000000,0,-1,11,0")
    label_style = ("chxs", "0,000000,11")
    data = ("chd","t:%s" % ','.join([str(item[data_key]) for item in data_list]))
    base_url = "http://chart.apis.google.com/chart?"
    query_params = (chart_type, chart_size, bar_size, scaling, marker_axis, marker_text,
                    marker_style, label_style, data)
    url = base_url + urllib.urlencode(query_params)
    return url

def piechart(data_dict, title=None):
    ''' produces a pie chart showing breakdown by category from either
    contributions or recipients information. the value contained in
    data_dict are expected to be STRINGS, representing percents
    (eg. between 0 and 100) '''

    for k,v in data_dict.iteritems():
        data_dict[k] = float(v)        
    # calculate each value as a percent of all values, and then
    # convert it to a string for url formatting.
    chart_data = [str(val/sum(data_dict.values())) for val in data_dict.values()]

    legend_text = []
    for i in xrange(len(data_dict)):
        # build a legend item for each slice in the pie, showing
        # titles and the values as percents, rounding to the nearest
        # whole percent.
        legend_text.append("%s (%s%%)" % (data_dict.keys()[i], int(round(float(chart_data[i])*100))))


    legend = "&chdl=%s" % '|'.join(legend_text)
    data = "&chd=t:%s" % ','.join(chart_data)
    url = "http://chart.apis.google.com/chart?cht=p&chs=250x150"+data+legend
    if title:
        chart_title = "&chtt=%s" % title
        url = url+chart_title
    return url


def timeline_sparkline(data_list):
    ''' generates a sparkline of contributions given or received over
    the time period represented by the '''
    if not len(data_list):
        return None
    max_value = max([float(item) for item in data_list])
    scaling = "&chds=0,%f" % max_value
    data = "&chd=t:%s" % ','.join(data_list)
    url = "http://chart.apis.google.com/chart?cht=ls&chs=100x30"+data+scaling
    return url

def raphael_demo(request):
    entity_id = "72dff1d2eacd4bf59283051f36ac4b61"
    api = AggregatesAPI()
    fake_data = api.breakdown('contributors', 'party')
    top_industries = api.top_industries(entity_id, cycle='2008')

    # Convert fake data back to integers (this should be done in
    # the API call instead if we decide to go with this solution). 
    for k in fake_data.keys():
        fake_data[k] = int(fake_data[k])
    return render_to_response('chart_demo.html',
                              {'data': fake_data,
                               'bar_data': top_industries,
                               },
                              entity_context(request))

def rtest(request):
    return render_to_response('rtest.html')

