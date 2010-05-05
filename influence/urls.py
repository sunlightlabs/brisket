from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.conf import settings

urlpatterns = patterns('brisket.influence.views',
    url(r'^search', 'search', name='search'),                       

    # industry                       
    url(r'^sector/[\w\-]+/(?P<entity_id>\w+)', 'sector_detail', 
        name='sector_detail'),                       

    # entity pages
    url(r'^organization/[\w\-]+/(?P<entity_id>\w+)', 'organization_entity', 
        name='organization_entity'),                       
    url(r'^politician/[\w\-]+/(?P<entity_id>\w+)', 'politician_entity', 
        name='politician_entity'),                       
    url(r'^individual/[\w\-]+/(?P<entity_id>\w+)', 'individual_entity', 
        name='individual_entity'),                       

    # utility
    url(r'^reset$', 'clear_network', name='clear_network'),                       

    # make sure this goes after the more specific urls or it will
    # match before the others get hit.
    url(r'^$', 'index', name='index'),                       
)

urlpatterns += patterns('django.views.generic.simple',
    # treat urls without the entity_id as search strings                           

    url(r'^organization/(?P<query_string>[\w\-]+)', 'redirect_to', 
        {'url': '/search?query=%(query_string)s&cycle=%(cycle)s'}),                       

    url(r'^politician/(?P<query_string>[\w\-]+)', 'redirect_to', 
        {'url': '/search?query=%(query_string)s&cycle=%(cycle)s'}),                       

    url(r'^individual/(?P<query_string>[\w\-]+)', 'redirect_to', 
        {'url': '/search?query=%(query_string)s&cycle=%(cycle)s'}),                       

)
