from dcapi.contracts.urls import contractsfilter_handler
from dcapi.contributions.urls import contributionfilter_handler
from dcapi.earmarks.urls import earmarkfilter_handler
from dcapi.grants.urls import grantsfilter_handler
from dcapi.lobbying.urls import lobbyingfilter_handler
from dcapi.contractor_misconduct.urls import contractor_misconduct_filter_handler

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dc_web.public.views',
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    
    # old filter redirect to contributions
    url(r'^filter/$', 'filter', name="filter"),
    
    # contracts
    url(r'^contracts/$', 'filter_contracts', name="filter_contracts"),
    url(r'^contracts/download/$', 'search_download', {'search_resource': contractsfilter_handler},  name="data_contracts_download"),
    url(r'^data/contracts/$', 'search_preview', {'search_resource': contractsfilter_handler}, name="data_contracts"),
    url(r'^data/contracts/count/$', 'search_count', {'search_resource': contractsfilter_handler}, name="data_contracts_count"),
    
    # contributions
    url(r'^contributions/$', 'filter_contributions', name="filter_contributions"),
    url(r'^contributions/download/$', 'search_download', {'search_resource': contributionfilter_handler},  name="data_contributions_download"),
    url(r'^data/contributions/$', 'search_preview', {'search_resource': contributionfilter_handler}, name="data_contributions"),
    url(r'^data/contributions/count/$', 'search_count', {'search_resource': contributionfilter_handler}, name="data_contributions_count"),
    
    # earmarks
    url(r'^earmarks/$', 'filter_earmarks', name="filter_earmarks"),
    url(r'^earmarks/download/$', 'search_download', {'search_resource': earmarkfilter_handler},  name="data_earmarks_download"),
    url(r'^data/earmarks/$', 'search_preview', {'search_resource': earmarkfilter_handler}, name="data_earmarks"),
    url(r'^data/earmarks/count/$', 'search_count', {'search_resource': earmarkfilter_handler}, name="data_earmarks_count"),
     
    # grants
    url(r'^grants/$', 'filter_grants', name="filter_grants"),
    url(r'^grants/download/$', 'search_download', {'search_resource': grantsfilter_handler},  name="data_grants_download"),
    url(r'^data/grants/$', 'search_preview', {'search_resource': grantsfilter_handler}, name="data_grants"),
    url(r'^data/grants/count/$', 'search_count', {'search_resource': grantsfilter_handler}, name="data_grants_count"),

    # lobbying
    url(r'^lobbying/$', 'filter_lobbying', name="filter_lobbying"),
    url(r'^lobbying/download/$', 'search_download', {'search_resource': lobbyingfilter_handler},  name="data_lobbying_download"),
    url(r'^data/lobbying/$', 'search_preview', {'search_resource': lobbyingfilter_handler}, name="data_lobbying"),
    url(r'^data/lobbying/count/$', 'search_count', {'search_resource': lobbyingfilter_handler}, name="data_lobbying_count"),
    
    # contractor_misconduct
    url(r'^contractor_misconduct/$', 'filter_contractor_misconduct', name="filter_contractor_misconduct"),
    url(r'^contractor_misconduct/download/$', 'search_download', {'search_resource': contractor_misconduct_filter_handler},  name="data_contractor_misconduct_download"),
    url(r'^data/contractor_misconduct/$', 'search_preview', {'search_resource': contractor_misconduct_filter_handler}, name="data_contractor_misconduct"),
    url(r'^data/contractor_misconduct/count/$', 'search_count', {'search_resource': contractor_misconduct_filter_handler}, name="data_contractor_misconduct_count"),
 
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
    url(r'^docs/earmarks/$', 'direct_to_template', {'template': 'docs/earmarks.html'}, name="doc_earmarks"),
    url(r'^docs/changelog/$', 'direct_to_template', {'template': 'docs/changelog.html'}, name="doc_changelog"),
)
