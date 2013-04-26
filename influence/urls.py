from django.conf.urls.defaults import patterns, url
from brisket.influence.sitemaps import sitemaps, index_wrapper, sitemap_wrapper

urlpatterns = patterns('brisket.influence.views',
    url(r'^search', 'search', name='search'),

    # industry
    # url(r'^sector/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'sector_detail',
    #     name='sector_detail'),

    # landing pages
    url(r'^organizations$', 'organization_landing'),
    url(r'^politicians$',   'politician_landing'),
    url(r'^people$',        'people_landing'),
    url(r'^industries$',    'industry_landing'),

    # entity previews (mainly for OpenRefine)
    url(r'^organization/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_preview', {'type': 'organization'}, name='entity_preview'),
    url(r'^politician/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_preview', {'type': 'politician'}, name='entity_preview'),
    url(r'^individual/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_preview', {'type': 'individual'}, name='entity_preview'),
    url(r'^entity/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_preview_redirect', name='entity_preview_redirect'),

    # entity pages
    url(r'^organization/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'organization_entity',
        name='organization_entity'),
    url(r'^politician/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'politician_entity',
        name='politician_entity'),
    url(r'^individual/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'individual_entity',
        name='individual_entity'),
    url(r'^industry/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'industry_entity',
        name='industry_entity'),
    url(r'^entity/(?P<entity_id>[a-f0-9-]{32,36})', 'entity_redirect', name='entity_redirect'),

    # utility
    #url(r'^reset$', 'clear_network', name='clear_network'),

    # make sure this goes after the more specific urls or it will
    # match before the others get hit.
    url(r'^$', 'index', name='index'),
)

urlpatterns += patterns('django.views.generic.simple',
    # treat urls without the entity_id as search strings

    url(r'^organization/(?P<query_string>[\w\-]+)', 'redirect_to',
        {'url': '/search?query=%(query_string)s'}),

    url(r'^politician/(?P<query_string>[\w\-]+)', 'redirect_to',
        {'url': '/search?query=%(query_string)s'}),

    url(r'^individual/(?P<query_string>[\w\-]+)', 'redirect_to',
        {'url': '/search?query=%(query_string)s'}),
    
    url(r'^industry/(?P<query_string>[\w\-]+)', 'redirect_to',
        {'url': '/search?query=%(query_string)s'}),

    url(r'^contact/?$', 'direct_to_template',
        {'template': 'contact.html'}),

    url(r'^about/?$', 'direct_to_template',
        {'template': 'about.html'}),
        
    url(r'^about/methodology/campaign_finance/?$', 'direct_to_template',
        {'template': 'campaign_finance_methodology.html'}),

    url(r'^about/methodology/lobbying/?$', 'direct_to_template',
        {'template': 'lobbying_methodology.html'}),
    
    url(r'^about/methodology/lobbyist_bundling/?$', 'direct_to_template',
        {'template': 'lobbyist_bundling_methodology.html'}),
                
    url(r'^about/methodology/fed_spending/?$', 'direct_to_template',
        {'template': 'fed_spending_methodology.html'}),
        
    url(r'^about/methodology/earmarks/?$', 'direct_to_template',
        {'template': 'earmark_methodology.html'}),

    url(r'^about/methodology/echo/?$', 'direct_to_template',
        {'template': 'epa_echo_methodology.html'}),
   
    url(r'^checking/?$', 'direct_to_template',
        {'template': 'checking.html'}),
)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', index_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
