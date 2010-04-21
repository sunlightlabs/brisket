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
    org_recipients = api.org_recipients(entity_id, cycle=cycle)
    #print org_recipients
    recipients_barchart_data = []
    for record in org_recipients:        
        recipients_barchart_data.append({
                'key': record['name'],
                'value' : record['total_amount'],
                # currently we only display politician recipients from
                # orgs. this should be changed if we start returning
                # org-to-org data.
                'href' : "/politician/%s" % record['id'],
                })

    party_breakdown = api.org_breakdown(entity_id, 'party', cycle)
    print party_breakdown
    for key, values in party_breakdown.iteritems():
        party_breakdown[key] = float(values[1])
    level_breakdown = api.org_breakdown(entity_id, 'level', cycle)
    print 'here!'
    print level_breakdown
    for key, values in level_breakdown.iteritems():
        level_breakdown[key] = float(values[1])

    # fake us some sparkline data
    amounts = [str(recipient['total_amount']) for recipient in org_recipients]
    sparkline = timeline_sparkline(amounts)
    return render_to_response('organization.html', 
                              {'entity_id': entity_id, 
                               'entity_info': entity_info,
                               'level_breakdown' : level_breakdown,
                               'party_breakdown' : party_breakdown,
                               'recipients_barchart_data': recipients_barchart_data,
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

    # top sectors is already sorted
    top_sectors = api.top_sectors(entity_id, cycle=cycle)
    sectors_barchart_data = []
    for record in top_sectors:        
        sectors_barchart_data.append({
                'key': record['sector_code'],
                'value' : record['amount'],
                'href' : "/industry/%s" % record['sector_code'],
                })

    local_breakdown = api.pol_breakdown(entity_id, 'local', cycle)
    for key, values in local_breakdown.iteritems():
        # values is a list of [count, amount]
        local_breakdown[key] = float(values[1])

    entity_breakdown = api.pol_breakdown(entity_id, 'entity', cycle)
    for key, values in entity_breakdown.iteritems():
        # values is a list of [count, amount]
        entity_breakdown[key] = float(values[1])    

    # fake sparkline data
    amounts = [str(contributor['amount']) for contributor in top_contributors]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('politician.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'top_contributors': top_contributors,
                               'local_breakdown' : local_breakdown,
                               'entity_breakdown' : entity_breakdown,
                               'sectors_barchart_data': sectors_barchart_data,
                               'sparkline': sparkline,
                               },
                              entity_context(request))
        
def individual_entity(request, entity_id):    
    # individuals only give contributions
    api = AggregatesAPI() 
    entity_info = api.entity_metadata(entity_id)    
    cycle = request.GET.get("cycle", 2010)

    recipient_candidates = api.indiv_recipients(entity_id, cycle=cycle, recipient_types='pol')
    recipient_orgs = api.indiv_recipients(entity_id, cycle=cycle, recipient_types='org')
    candidates_barchart = topn_barchart(recipient_candidates, label_key = 'name', data_key = 'amount')
    orgs_barchart = topn_barchart(recipient_orgs, label_key = 'name', data_key = 'amount')    
    party_breakdown = api.indiv_breakdown(entity_id, 'party', cycle)
    for key, values in party_breakdown.iteritems():
        # values is a list of [count, amount]
        party_breakdown[key] = values[1]    
    piechart_party = piechart(party_breakdown, "Republicans vs. Democrats")

    # fake sparkline data
    amounts = [str(contributor['amount']) for contributor in recipient_candidates]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('individual.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'candidates_barchart': candidates_barchart,
                               'orgs_barchart': orgs_barchart,
                               'pie_chart_party' : piechart_party, 
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
    print 'sparkline data'
    print data_list
    max_value = max([float(item) for item in data_list])
    scaling = "&chds=0,%f" % max_value
    data = "&chd=t:%s" % ','.join(data_list)
    url = "http://chart.apis.google.com/chart?cht=ls&chs=100x30"+data+scaling
    return url

def raphael_demo(request):
    entity_id = "72dff1d2eacd4bf59283051f36ac4b61"
    api = AggregatesAPI()
    top_industries = api.top_sectors(entity_id, cycle='2008')
    fake_data = {'label1': 77, 'label2': 23}
    return render_to_response('chart_demo.html',
                              {'data': fake_data,
                               'bar_data': top_industries,
                               },
                              entity_context(request))

def rtest(request):
    return render_to_response('rtest.html')

