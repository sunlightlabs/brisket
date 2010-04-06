from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^search', 'influence.views.search', name='search'),                       
    url(r'^(organization|pac)/(?P<entity_id>.+)', 'influence.views.organization_entity', 
        name='organization_entity'),                       
    url(r'^politician/(?P<entity_id>.+)', 'influence.views.politician_entity', 
        name='politician_entity'),                       
    url(r'^individual/(?P<entity_id>.+)', 'influence.views.individual_entity', 
        name='politician_entity'),                       
    # make sure this goes after the more specific urls or it will
    # match before the others get hit.
    url(r'^', 'influence.views.index', name='index'),                       
)
