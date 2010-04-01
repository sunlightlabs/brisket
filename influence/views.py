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

from brisket.influence.forms import SearchForm
from lib import AggregatesAPI, InfluenceNetworkBuilder

def index(request):    
    search_form = SearchForm()
    return render_to_response('index.html', {'form':search_form})

def search(request):
    if not request.GET.get('query', None):
        print 'Form Error'
        self.HttpResponseRedirect('/')
    
    submitted_form = SearchForm(request.GET)
    if submitted_form.is_valid():        
        api = AggregatesAPI()
        results = api.entity_search(submitted_form.cleaned_data['query'])
        entity_results = [result for result in results if result['id']]
        return render_to_response('results.html', {'results': entity_results})
    else: 
        form = SearchForm(request.GET)
        return HttpResponseRedirect('/')

def organization_entity(request, entity_id):
    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)

    # organizations both give and receive contributions
    top_contributors = api.top_contributors(entity_id)
    top_recipients = api.top_recipients(entity_id)

    fake_piechart_data = {
        'In State' : str(32.7),
        'Out of State' : str(100.0-32.7)
        }
    pie_chart = breakdown_piechart(fake_piechart_data)

    #contributions_barchart = topn_barchart(top_contributors)
    #recipients_barchart = topn_barchart(top_recipients)

    return render_to_response('organization.html', {'entity_id': entity_id, 
                                                    'entity_info': entity_info,
                                                    'top_contributors': top_contributors, 
                                                    'top_recipients': top_recipients, 
                                                    'pie_chart' : pie_chart,
     #                                               'contributions_barchart': contributions_barchart,
     #                                               'recipients_barchart': recipients_barchart,
                                                    })

def politician_entity(request, entity_id):

    api = AggregatesAPI()    
    entity_info = api.entity_metadata(entity_id)
    top_contributors = api.top_contributors(entity_id)
    # politicians only receive contributions

    fake_piechart_instate = {
        'In State' : str(32.7),
        'Out of State' : str(100.0-32.7)
        }
    pie_chart_instate = breakdown_piechart(fake_piechart_instate, "In State vs. Out of State")

    fake_piechart_source = {
        'Individuals' : str(17.7),
        'PACs' : str(100.0-17.7)
        }
    pie_chart_source = breakdown_piechart(fake_piechart_source, "Individuals vs. PACs")

    contributions_barchart = topn_barchart(top_contributors)

    return render_to_response('politician.html', {'entity_id': entity_id,
                                                  'entity_info': entity_info,
                                                  'top_contributors': top_contributors,
                                                  'pie_chart_instate' : pie_chart_instate,
                                                  'pie_chart_source' : pie_chart_source,
                                                  'contributions_barchart': contributions_barchart,
                                                  })
        
def individual_entity(request, entity_id):
    
    # individuals only give contributions

    return render_to_response('individual.html', {'entity_id': entity_id})

def topn_barchart(data_list):
    ''' generates a horizontal bargraph of aggregate contribution data. '''
    if not data_list:
        return None
    max_value = max([float(item['amount']) for item in data_list])
    scaling = "&chds=0,%f" % max_value
    print "max value: %d" % float(max_value)
    labels = "&chxt=y&chxl=0:|%s" % '|'.join([str(item['name']) for item in data_list])
    label_style = "&chxs=0,000000,8"
    data = "&chd=t:%s" % ','.join([str(item['amount']) for item in data_list])
    markers = "&chm=N*cUSD*,000000,0,-1,11,0"
    url = "http://chart.apis.google.com/chart?cht=bhs&chs=250x150&chbh=a"+markers+labels+label_style+data+scaling
    return url

def breakdown_piechart(data_dict, title=None):
    ''' produces a pie chart showing breakdown by category from either
    contributions or recipients information. the value contained in
    data_dict are expected to be STRINGS, representing percents
    (eg. between 0 and 100) '''

    legend = "&chdl=%s" % '|'.join(data_dict.keys())
    data = "&chd=t:%s" % ','.join(data_dict.values())
    background = "&chf=bg,s,93a8b0"
    url = "http://chart.apis.google.com/chart?cht=p&chs=250x150"+data+legend+background
    if title:
        chart_title = "&chtt=%s" % title
        url = url+chart_title
    return url


def timeline_sparkline(data_list):
    ''' generates a sparkline of contributions given or received over
    the time period represented by the '''
    pass
