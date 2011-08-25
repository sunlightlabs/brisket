from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('brisket.fec.views',
    url(r'^$', direct_to_template, {'template': 'fec/index.html'}),
    url('^senate.json$', 'get_json', {'file': 'data/senate.csv'}),
    url('^house.json$', 'get_json', {'file': 'data/house.csv'}),
)
