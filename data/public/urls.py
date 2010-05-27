from django.conf.urls.defaults import *

urlpatterns = patterns('dc_web.public.views',
    url(r'^api/$', 'api_index', name="api_index"),
    url(r'^api/aggregates/contributions/$', 'api_aggregate_contributions', name="api_aggregate_contributions"),
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    
    # old filter redirect to contributions
    url(r'^filter/$', 'filter', name="filter"),
    
    # contributions
    url(r'^contributions/$', 'filter_contributions', name="filter_contributions"),
    url(r'^contributions/download/$', 'data_contributions_download', name="data_contributions_download"),
    url(r'^data/contributions/$', 'data_contributions', name="data_contributions"),
    url(r'^data/contributions/count/$', 'data_contributions', {'count': True}, name="data_contributions_count"),
    url(r'^debug/contributions/$', 'debug_contributions', name="debug_contributions"),
    
    # grants
    url(r'^grants/$', 'filter_grants', name="filter_grants"),
    url(r'^grants/download/$', 'data_grants_download', name="data_grants_download"),
    url(r'^data/grants/$', 'data_grants', name="data_grants"),
    url(r'^data/grants/count/$', 'data_grants', {'count': True}, name="data_grants_count"),
    url(r'^debug/grants/$', 'debug_grants', name="debug_grants"),
    
    # lobbying
    url(r'^lobbying/$', 'filter_lobbying', name="filter_lobbying"),
    url(r'^lobbying/download/$', 'data_lobbying_download', name="data_lobbying_download"),
    url(r'^data/lobbying/$', 'data_lobbying', name="data_lobbying"),
    url(r'^data/lobbying/count/$', 'data_lobbying', {'count': True}, name="data_lobbying_count"),
    url(r'^debug/lobbying/$', 'debug_lobbying', name="debug_lobbying"),
    
    url(r'^$', 'index', name="index"),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^docs/$', 'direct_to_template', {'template': 'docs/index.html'}, name="doc_index"),
    url(r'^docs/contributions/$', 'direct_to_template', {'template': 'docs/contributions.html'}, name="doc_contributions"),
    url(r'^docs/grants/$', 'direct_to_template', {'template': 'docs/grants.html'}, name="doc_grants"),
    url(r'^docs/lobbying/$', 'direct_to_template', {'template': 'docs/lobbying.html'}, name="doc_lobbying"),
)