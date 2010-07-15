from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.conf import settings

urlpatterns = patterns('brisket.influence.views',
    url(r'^search', 'search', name='search'),

    # industry
    # url(r'^sector/[\w\-]+/(?P<entity_id>\w+)', 'sector_detail',
    #     name='sector_detail'),

    # landing pages
    url(r'^organizations$', 'organization_landing'),
    url(r'^politicians$',   'politician_landing'),
    url(r'^people$',        'people_landing'),

    # entity pages
    url(r'^organization/[\w\-]+/(?P<entity_id>\w+)', 'organization_entity',
        name='organization_entity'),
    url(r'^politician/[\w\-]+/(?P<entity_id>\w+)', 'politician_entity',
        name='politician_entity'),
    url(r'^individual/[\w\-]+/(?P<entity_id>\w+)', 'individual_entity',
        name='individual_entity'),

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

    url(r'^contact/$', 'direct_to_template',
        {'template': 'contact.html'}),

    url(r'^about/$', 'direct_to_template',
        {'template': 'about.html'}),
        
    url(r'^about/methodology/campaign_finance/$', 'direct_to_template',
        {'template': 'campaign_finance_methodology.html'}),
)
