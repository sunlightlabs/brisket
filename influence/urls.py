from django.conf.urls import patterns, url
from brisket.influence.sitemaps import sitemaps, index_wrapper, sitemap_wrapper
from brisket.influence.views import PoliticianEntityView, IndividualEntityView, OrganizationEntityView, IndustryEntityView, PoliticianPreviewView
from brisket.influence.views import IndustryLandingView, OrgLandingView, \
                                    PolGroupLandingView, LobbyingOrgLandingView,\
                                    IndividualLandingView, LobbyistLandingView, \
                                    PolLandingView, search_redirect, \
                                    bioguide_redirect, fuzzy_match_view

from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('brisket.influence.views',
    url(r'^search$', 'search', name='search', kwargs={'search_type': 'all', 'search_subtype': 'all'}),
    url(r'^search/(?P<search_type>[a-z]+)$', 'search', name='search', kwargs={'search_subtype': 'all'}),
    url(r'^search/(?P<search_type>[a-z]+)/(?P<search_subtype>[a-z_]+)$', 'search', name='search'),

    # industry
    # url(r'^sector/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})', 'sector_detail',
    #     name='sector_detail'),

    # entity landing pages
    # -> groups
    url(r'^industries$', IndustryLandingView.as_view()),
    url(r'^organizations$', OrgLandingView.as_view()),
    url(r'^political-groups$', PolGroupLandingView.as_view()),
    url(r'^lobbying-orgs$', LobbyingOrgLandingView.as_view()),
    # -> people
    url(r'^individuals$', IndividualLandingView.as_view()),
    url(r'^lobbyists$', LobbyistLandingView.as_view()),
    url(r'^politicians$', PolLandingView.as_view()),

    # other landing pages
    # -> places
    url(r'^cities$', 'city_landing'),
    url(r'^states$', 'state_landing'),
    # -> collections
    url(r'^collections/campaign-finance', 'campaign_finance_landing'),
    url(r'^collections/lobbying', 'lobbying_landing'),
    url(r'^collections/regulations', 'regs_landing'),
    url(r'^collections/federal-spending', 'fed_spending_landing'),
    url(r'^collections/contractor-misconduct', 'contractor_misconduct_landing'),
    url(r'^collections/epa-violations', 'epa_echo_landing'),
    url(r'^collections/advisory-committees', 'faca_landing'),

    # entity previews (mainly for OpenRefine)
    url(r'^organization/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_redirect', name='organization_preview'),
    url(r'^politician/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})/preview', PoliticianPreviewView.as_view(), name='politician_preview'),
    url(r'^individual/[\w\-]+/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_redirect', name='individual_preview'),
    url(r'^entity/(?P<entity_id>[a-f0-9-]{32,36})/preview', 'entity_preview_redirect', name='entity_preview_redirect'),


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

urlpatterns += patterns('',
    # treat urls without the entity_id as search strings

    url(r'^(?P<entity_type>(individual|politician|organization|industry|entity)+)/(?P<query_string>[\w\-]+)$', search_redirect),

    url(r'^bioguide/(?P<bioguide_id>[a-zA-Z][0-9]{6})$', bioguide_redirect),
    
    url(r'^fuzzy$', fuzzy_match_view),

    url(r'^people$', RedirectView.as_view(url='/individuals')), # backwards compatability redirect
    
    url(r'^contributors$', RedirectView.as_view(url='/individuals')), # backwards compatability redirect

    url(r'^contact/?$', TemplateView.as_view(template_name='contact.html')),

    url(r'^about/?$', TemplateView.as_view(template_name='about.html')),
        
    url(r'^about/methodology/campaign_finance/?$', TemplateView.as_view(template_name='methodology/campaign_finance_methodology.html')),

    url(r'^about/methodology/lobbying/?$', TemplateView.as_view(template_name='methodology/lobbying_methodology.html')),
    
    url(r'^about/methodology/lobbyist_bundling/?$', TemplateView.as_view(template_name='methodology/lobbyist_bundling_methodology.html')),
                
    url(r'^about/methodology/fed_spending/?$', TemplateView.as_view(template_name='methodology/fed_spending_methodology.html')),
        
    url(r'^about/methodology/earmarks/?$', TemplateView.as_view(template_name='methodology/earmark_methodology.html')),

    url(r'^about/methodology/echo/?$', TemplateView.as_view(template_name='methodology/epa_echo_methodology.html')),
   
    url(r'^checking/?$', TemplateView.as_view(template_name='checking.html')),
)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', index_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
