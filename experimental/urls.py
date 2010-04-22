from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('brisket.experimental.views',
    url(r'^search', 'search', name='search'),                       

    # detail pages                       
    url(r'^politician/(?P<entity_id>.+)/details', 'industry_detail', 
        name='industry_detail'),                       
    url(r'^(organization|pac)/(?P<entity_id>.+)/details', 'industry_detail', 
        name='industry_detail'),                       

    # entity pages
    url(r'^(organization|pac)/(?P<entity_id>.+)', 'organization_entity', 
        name='organization_entity'),                       
    url(r'^politician/(?P<entity_id>.+)', 'politician_entity', 
        name='politician_entity'),                       
    url(r'^individual/(?P<entity_id>.+)', 'individual_entity', 
        name='politician_entity'),                       

    # make sure this goes after the more specific urls or it will
    # match before the others get hit.
    url(r'^', 'index', name='index'),                       
)
