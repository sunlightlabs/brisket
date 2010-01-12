from django.conf.urls.defaults import *

urlpatterns = patterns('dc_web.public.views',
    url(r'^api/$', 'api_index', name="api_index"),
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    url(r'^docs/$', 'doc_index', name="doc_index"),
    url(r'^filter/$', 'filter', name="filter"),
    url(r'^data/contributions/$', 'data_contributions', name="data_contributions"),
    url(r'^data/contributions/download/$', 'data_contributions_download', name="data_contributions_download"),
    url(r'^data/entities/(?P<entity_type>contributor|recipient|organization|committee|quick)/$', 'data_entities', name="data_entities"),
    url(r'^debug/contributions/$', 'debug_contributions', name="debug_contributions"),
    url(r'^$', 'index', name="index"),
)
