from django.conf.urls.defaults import *

urlpatterns = patterns('dc_web.public.views',
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    
    # old filter redirect to contributions
    url(r'^filter/$', 'filter', name="filter"),
    
    # grants
    url(r'^contracts/$', 'filter_contracts', name="filter_contracts"),
    url(r'^contracts/download/$', 'data_contracts_download', name="data_contracts_download"),
    url(r'^data/contracts/$', 'data_contracts', name="data_contracts"),
    url(r'^data/contracts/count/$', 'data_contracts', {'count': True}, name="data_contracts_count"),
    url(r'^debug/contracts/$', 'debug_contracts', name="debug_contracts"),
    
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
    
    # doc lookups
    url(r'^docs/lookup/(?P<dataset>\w+)/(?P<field>[\w\-_]+)/$', 'lookup', name="doc_lookup"),
    
    url(r'^$', 'index', name="index"),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^api/$', 'direct_to_template', {'template': 'api/index.html'}, name="api_index"),
    url(r'^api/contracts/$', 'direct_to_template', {'template': 'api/contracts.html'}, name="api_contracts"),
    url(r'^api/contributions/$', 'direct_to_template', {'template': 'api/contributions.html'}, name="api_contributions"),
    url(r'^api/grants/$', 'direct_to_template', {'template': 'api/grants.html'}, name="api_grants"),
    url(r'^api/lobbying/$', 'direct_to_template', {'template': 'api/lobbying.html'}, name="api_lobbying"),
    url(r'^api/aggregates/contributions/$', 'direct_to_template', {'template': 'api/aggregates_contributions.html'}, name="api_aggregate_contributions"),
    url(r'^docs/$', 'direct_to_template', {'template': 'docs/index.html'}, name="doc_index"),
    url(r'^docs/contracts/$', 'direct_to_template', {'template': 'docs/contracts.html'}, name="doc_contracts"),
    url(r'^docs/contributions/$', 'direct_to_template', {'template': 'docs/contributions.html'}, name="doc_contributions"),
    url(r'^docs/grants/$', 'direct_to_template', {'template': 'docs/grants.html'}, name="doc_grants"),
    url(r'^docs/lobbying/$', 'direct_to_template', {'template': 'docs/lobbying.html'}, name="doc_lobbying"),
)