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
    return RequestContext(request, {'search_form': SearchForm(), 
                                    'cycle_form': ElectionCycle(), 
                                    })

def index(request):    
    return render_to_response('index.html', brisket_context(request))

def search(request):
    if not request.GET.get('query', None):
        print 'Form Error'
        self.HttpResponseRedirect('/')
    
    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        api = AggregatesAPI()
        results = api.entity_search(submitted_form.cleaned_data['query'])
        entity_results = [result for result in results if result['id']]
        return render_to_response('results.html', {'results': entity_results}, 
                                  brisket_context(request))
    else: 
        form = SearchForm(request.GET)
        return HttpResponseRedirect('/')

def organization_entity(request, entity_id):
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    # organizations both give and receive contributions
    top_contributors = api.top_contributors(entity_id)
    top_recipients = api.top_recipients(entity_id)
    pie_chart_party = breakdown_piechart(api.breakdown('recipients', 'party'), 
                                         "Republicans vs. Democrats")
    pie_chart_level = breakdown_piechart(api.breakdown('recipients', 'level'),
                                         "State vs. Federal")

    candidates_barchart = topn_barchart(top_recipients)
    amounts = [str(recipient['amount']) for recipient in top_recipients]
    sparkline = timeline_sparkline(amounts)

    return render_to_response('organization.html', 
                              {'entity_id': entity_id, 
                               'entity_info': entity_info,
                               'top_contributors': top_contributors, 
                               'top_recipients': top_recipients, 
                               'pie_chart_level' : pie_chart_level,
                               'pie_chart_party' : pie_chart_party,
                               'candidates_barchart': candidates_barchart,
                               'sparkline': sparkline,
                               },
                              entity_context(request))

def politician_entity(request, entity_id):
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    # politicians only receive contributions
    top_contributors = api.top_contributors(entity_id)
    pie_chart_instate = breakdown_piechart(api.breakdown('contributors', 'instate'),
                                           "In State vs. Out of State")
    fake_piechart_source = {
        'Individuals' : str(17.7),
        'PACs' : str(100.0-17.7)
        }
    pie_chart_source = breakdown_piechart(fake_piechart_source, "Individuals vs. PACs")
    contributors_barchart = topn_barchart(top_contributors)
    amounts = [str(contributor['amount']) for contributor in top_contributors]
    sparkline = timeline_sparkline(amounts)
    return render_to_response('politician.html', 
                              {'entity_id': entity_id,
                               'entity_info': entity_info,
                               'top_contributors': top_contributors,
                               'pie_chart_instate' : pie_chart_instate,
                               'pie_chart_source' : pie_chart_source,
                               'contributors_barchart': contributors_barchart,
                               'sparkline': sparkline,
                               },
                              entity_context(request))
        
def individual_entity(request, entity_id):    
    # individuals only give contributions
    return render_to_response('individual.html', {'entity_id': entity_id},
                              entity_context(request))

def topn_barchart(data_list):
    ''' generates a horizontal bargraph of aggregate contribution data. '''
    if not data_list:
        return None
    max_value = max([float(item['amount']) for item in data_list])

    # compile the query parameters as tuples which will be urlencoded
    # before being appended to the chart url.
    chart_type = ("cht", "bhs")
    chart_size = ("chs", "250x150")
    bar_size = ("chbh", "a")
    scaling = ("chds", "0,%f" % max_value)
    marker_axis = ("chxt", "y")
    marker_text = ("chxl", "0:|%s" % '|'.join([item['name'] for item in data_list]))
    marker_style = ("chm", "N*cUSD*,000000,0,-1,11,0")
    label_style = ("chxs", "0,000000,8")
    data = ("chd","t:%s" % ','.join([str(item['amount']) for item in data_list]))
    base_url = "http://chart.apis.google.com/chart?"
    query_params = (chart_type, chart_size, bar_size, scaling, marker_axis, marker_text,
                    marker_style, label_style, data)
    url = base_url + urllib.urlencode(query_params)
    return url

def breakdown_piechart(data_dict, title=None):
    ''' produces a pie chart showing breakdown by category from either
    contributions or recipients information. the value contained in
    data_dict are expected to be STRINGS, representing percents
    (eg. between 0 and 100) '''

    legend = "&chdl=%s" % '|'.join(data_dict.keys())
    data = "&chd=t:%s" % ','.join(data_dict.values())
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
