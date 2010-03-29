from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^search', 'influence.views.search', name='search'),                       
    # make sure this goes after the search url or it will match before search gets hit.
    url(r'^organization/(?P<entity_id>.+)', 'influence.views.organization_entity', 
        name='organization_entity'),                       
    url(r'^politician/(?P<entity_id>.+)', 'influence.views.politician_entity', 
        name='organization_entity'),                       
    url(r'^', 'influence.views.index', name='index'),                       
)
