from django.conf.urls.defaults import patterns, url
from brisket.influence.sitemaps import sitemaps, index_wrapper, sitemap_wrapper
from brisket.influence.views import PoliticianEntityView, IndividualEntityView, OrganizationEntityView, IndustryEntityView

urlpatterns = patterns('brisket.influence.views',
    url(r'^search', 'search', name='search'),

    # industry
    # url(r'^sector/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'sector_detail',
    #     name='sector_detail'),

    # landing pages
    # -> groups
    url(r'^industries$', 'industry_landing'),
    url(r'^organizations$', 'organization_landing'),
    url(r'^political-groups$', 'pol_group_landing'),
    url(r'^lobbying-firms$', 'lobbying_firm_landing'),
    # -> places
    url(r'^cities$', 'city_landing'),
    url(r'^states$', 'state_landing'),
    # -> people
    url(r'^contributors$', 'contributor_landing'),
    url(r'^lobbyists$', 'lobbyist_landing'),
    url(r'^politicians$', 'politician_landing'),
    # -> collections
    url(r'^collections/campaign-finance', 'campaign_finance_landing'),
    url(r'^collections/lobbying', 'lobbying_landing'),
    url(r'^collections/regulations', 'regs_landing'),
    url(r'^collections/federal-spending', 'fed_spending_landing'),
    url(r'^collections/contractor-misconduct', 'contractor_misconduct_landing'),
    url(r'^collections/epa-violations', 'epa_echo_landing'),
    url(r'^collections/advisory-committees', 'faca_landing'),

    # entity pages
    url(r'^organization/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', OrganizationEntityView.as_view(),
        name='organization_entity'),
    url(r'^politician/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', PoliticianEntityView.as_view(),
        name='politician_entity'),
    url(r'^individual/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', IndividualEntityView.as_view(),
        name='individual_entity'),
    url(r'^industry/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', IndustryEntityView.as_view(),
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

    url(r'^people$', 'redirect_to', {'url': '/contributors'}), # backwards compatability redirect

    url(r'^contact/?$', 'direct_to_template',
        {'template': 'contact.html'}),

    url(r'^about/?$', 'direct_to_template',
        {'template': 'about.html'}),
        
    url(r'^about/methodology/campaign_finance/?$', 'direct_to_template',
        {'template': 'methodology/campaign_finance_methodology.html'}),

    url(r'^about/methodology/lobbying/?$', 'direct_to_template',
        {'template': 'methodology/lobbying_methodology.html'}),
    
    url(r'^about/methodology/lobbyist_bundling/?$', 'direct_to_template',
        {'template': 'methodology/lobbyist_bundling_methodology.html'}),
                
    url(r'^about/methodology/fed_spending/?$', 'direct_to_template',
        {'template': 'methodology/fed_spending_methodology.html'}),
        
    url(r'^about/methodology/earmarks/?$', 'direct_to_template',
        {'template': 'methodology/earmark_methodology.html'}),

    url(r'^about/methodology/echo/?$', 'direct_to_template',
        {'template': 'methodology/epa_echo_methodology.html'}),
   
    url(r'^checking/?$', 'direct_to_template',
        {'template': 'checking.html'}),
)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', index_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
