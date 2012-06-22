#from dcapi.contracts.urls import contractsfilter_handler
#from dcapi.contributions.urls import contributionfilter_handler
#from dcapi.earmarks.urls import earmarkfilter_handler
#from dcapi.grants.urls import grantsfilter_handler
#from dcapi.lobbying.urls import lobbyingfilter_handler
#from dcapi.contractor_misconduct.urls import contractor_misconduct_filter_handler

from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django.views.generic.simple import redirect_to

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
    
    # epa_echo
    url(r'^epa_echo/$', 'filter_epa_echo', name="filter_epa_echo"),
    
    # faca
    url(r'^faca/$', 'filter_faca', name="filter_faca"),
    
    # bundled contributions
    url(r'^contributions/bundled/$', 'filter_bundling', name="filter_bundling"),
 
    # doc lookups
#   url(r'^docs/lookup/(?P<dataset>\w+)/(?P<field>[\w\-_]+)/$', 'lookup', name="doc_lookup"),
    url(r'^index.php$', redirect_to, {'url': '/'}),
    
    url(r'^$', 'index', name="index"),
)

from collections import namedtuple
Section = namedtuple('Section', ['path', 'name', 'title'])

API_SECTIONS = [
    Section('/api/', 'api_index', 'Overview'),
    Section('/api/contributions/', 'api_contributions', 'Campaign Contributions'),
    Section('/api/lobbying/', 'api_lobbying', 'Federal Lobbying'),
    Section('/api/grants/', 'api_grants', 'Federal Grants'),
    Section('/api/contracts/', 'api_contracts', 'Federal Contracts'),
    Section('/api/aggregates/contributions/', 'api_aggregate_contributions', 'Aggregate Contributions'),
]

DOCS_SECTIONS = [
    Section('/docs/', 'docs_index', 'Overview'),
    Section('/docs/contributions/', 'docs_contributions', 'Campaign Finance'),
    Section('/docs/lobbying/', 'docs_lobbying', 'Federal Lobbying'),
    Section('/docs/grants/', 'docs_grants', 'Federal Grants'),
    Section('/docs/contracts/', 'docs_contracts', 'Federal Contracts'),
    Section('/docs/earmarks/', 'docs_earmarks', 'Earmarks'),
    Section('/docs/echo/', 'docs_echo', 'EPA ECHO'),
    Section('/docs/changelog/', 'docs_changelog', 'Data Changelog'),
]

for doc_page in API_SECTIONS + DOCS_SECTIONS:
    urlpatterns += patterns('django.views.generic.simple',
        url(
            '^%s?$' % doc_page.path[1:], # the ? makes the trailing slash optional
            'direct_to_template',
            {'template': 'data/' + '/'.join(doc_page.name.split('_', 1)) + '.html', 'extra_context': {'API_SECTIONS': API_SECTIONS, 'DOCS_SECTIONS': DOCS_SECTIONS}},
            name=doc_page.name,
        ),
    )

if settings.DEBUG:
    # evil URL for data
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
                'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    )

handler404 = 'brisket.views.page_not_found'
handler500 = 'brisket.views.server_error'
