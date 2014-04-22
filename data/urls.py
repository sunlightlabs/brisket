#from dcapi.contracts.urls import contractsfilter_handler
#from dcapi.contributions.urls import contributionfilter_handler
#from dcapi.earmarks.urls import earmarkfilter_handler
#from dcapi.grants.urls import grantsfilter_handler
#from dcapi.lobbying.urls import lobbyingfilter_handler
#from dcapi.contractor_misconduct.urls import contractor_misconduct_filter_handler

from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django.views.generic import RedirectView
from brisket.data.views import DirectTemplateView

urlpatterns = patterns('brisket.data.views',
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    
    # old filter redirect to contributions
    url(r'^filter/$', 'filter', name="filter"),
    
    # contracts
    url(r'^contracts/$', 'filter_contracts', name="filter_contracts"),
    
    # contributions
    url(r'^contributions/$', 'filter_contributions', name="filter_contributions"),

    # contributions DC
    url(r'^contributions/dc/$', 'filter_contributions_dc', name="filter_contributions_dc"),

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
    url(r'^index.php$', RedirectView.as_view(url='/')),
    
    url(r'^$', 'index', name="index"),
)

from collections import namedtuple
Section = namedtuple('Section', ['path', 'name', 'title'])

API_SECTIONS = [
    Section('/api/', 'api_index', 'Overview'),
    Section('/api/contributions/', 'api_contributions', 'Campaign Contributions'),
    Section('/api/contributions/dc/', 'api_contributions_dc', 'Campaign Contributions (DC)'),
    Section('/api/lobbying/', 'api_lobbying', 'Federal Lobbying'),
    Section('/api/grants/', 'api_grants', 'Federal Grants'),
    Section('/api/contracts/', 'api_contracts', 'Federal Contracts'),
    Section('/api/aggregates/contributions/', 'api_aggregate_contributions', 'Aggregate Contributions'),
]

DOCS_SECTIONS = [
    Section('/docs/', 'docs_index', 'Overview'),
    Section('/docs/contributions/', 'docs_contributions', 'Campaign Finance'),
    Section('/docs/contributions/dc', 'docs_contributions_dc', 'Campaign Finance (DC)'),
    Section('/docs/lobbying/', 'docs_lobbying', 'Federal Lobbying'),
    Section('/docs/grants/', 'docs_grants', 'Federal Grants'),
    Section('/docs/contracts/', 'docs_contracts', 'Federal Contracts'),
    Section('/docs/earmarks/', 'docs_earmarks', 'Earmarks'),
    Section('/docs/echo/', 'docs_echo', 'EPA ECHO'),
    Section('/docs/changelog/', 'docs_changelog', 'Data Changelog'),
    Section('/docs/foreign_lobbying/', 'docs_foreign_lobbying', 'Foreign Lobbying'),
]

for doc_page in API_SECTIONS + DOCS_SECTIONS:
    urlpatterns += patterns('',
        url(
            '^%s?$' % doc_page.path[1:], # the ? makes the trailing slash optional
            DirectTemplateView.as_view(template_name='data/' + '/'.join(doc_page.name.split('_', 1)) + '.html', extra_context={'API_SECTIONS': API_SECTIONS, 'DOCS_SECTIONS': DOCS_SECTIONS}),
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
