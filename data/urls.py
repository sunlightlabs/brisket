#from dcapi.contracts.urls import contractsfilter_handler
#from dcapi.contributions.urls import contributionfilter_handler
#from dcapi.earmarks.urls import earmarkfilter_handler
#from dcapi.grants.urls import grantsfilter_handler
#from dcapi.lobbying.urls import lobbyingfilter_handler
#from dcapi.contractor_misconduct.urls import contractor_misconduct_filter_handler

from django.conf.urls.defaults import patterns, url
from django.conf import settings

urlpatterns = patterns('brisket.data.views',
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    
    # old filter redirect to contributions
    url(r'^filter/$', 'filter', name="filter"),
    
    # contracts
    url(r'^contracts/$', 'filter_contracts', name="filter_contracts"),
    
    # contributions
    url(r'^contributions/$', 'filter_contributions', name="filter_contributions"),
    
    # earmarks
    url(r'^earmarks/$', 'filter_earmarks', name="filter_earmarks"),
     
    # grants
    url(r'^grants/$', 'filter_grants', name="filter_grants"),

    # lobbying
    url(r'^lobbying/$', 'filter_lobbying', name="filter_lobbying"),
    
    # contractor_misconduct
    url(r'^contractor_misconduct/$', 'filter_contractor_misconduct', name="filter_contractor_misconduct"),
 
    # doc lookups
#   url(r'^docs/lookup/(?P<dataset>\w+)/(?P<field>[\w\-_]+)/$', 'lookup', name="doc_lookup"),
    
    url(r'^$', 'index', name="index"),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^api/$', 'direct_to_template', {'template': 'data/api/index.html'}, name="api_index"),
    url(r'^api/contracts/$', 'direct_to_template', {'template': 'data/api/contracts.html'}, name="api_contracts"),
    url(r'^api/contributions/$', 'direct_to_template', {'template': 'data/api/contributions.html'}, name="api_contributions"),
    url(r'^api/grants/$', 'direct_to_template', {'template': 'data/api/grants.html'}, name="api_grants"),
    url(r'^api/lobbying/$', 'direct_to_template', {'template': 'data/api/lobbying.html'}, name="api_lobbying"),
    url(r'^api/aggregates/contributions/$', 'direct_to_template', {'template': 'data/api/aggregates_contributions.html'}, name="api_aggregate_contributions"),
    url(r'^docs/$', 'direct_to_template', {'template': 'data/docs/index.html'}, name="doc_index"),
    url(r'^docs/contracts/$', 'direct_to_template', {'template': 'data/docs/contracts.html'}, name="doc_contracts"),
    url(r'^docs/contributions/$', 'direct_to_template', {'template': 'data/docs/contributions.html'}, name="doc_contributions"),
    url(r'^docs/grants/$', 'direct_to_template', {'template': 'data/docs/grants.html'}, name="doc_grants"),
    url(r'^docs/lobbying/$', 'direct_to_template', {'template': 'data/docs/lobbying.html'}, name="doc_lobbying"),
    url(r'^docs/earmarks/$', 'direct_to_template', {'template': 'data/docs/earmarks.html'}, name="doc_earmarks"),
    url(r'^docs/changelog/$', 'direct_to_template', {'template': 'data/docs/changelog.html'}, name="doc_changelog"),
)

if settings.DEBUG:
    # evil URL for data
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
                'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    )
