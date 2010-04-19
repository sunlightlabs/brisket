from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^search', 'influence.views.search', name='search'),                       

    # detail pages                       
    url(r'^politician/(?P<entity_id>.+)/details', 'influence.views.industry_detail', 
        name='industry_detail'),                       
    url(r'^(organization|pac)/(?P<entity_id>.+)/details', 'influence.views.industry_detail', 
        name='industry_detail'),                       

    # entity pages
    url(r'^(organization|pac)/(?P<entity_id>.+)', 'influence.views.organization_entity', 
        name='organization_entity'),                       
    url(r'^politician/(?P<entity_id>.+)', 'influence.views.politician_entity', 
        name='politician_entity'),                       
    url(r'^individual/(?P<entity_id>.+)', 'influence.views.individual_entity', 
        name='politician_entity'),                       

    # chart demos
    url(r'^charts/raphael', 'influence.views.raphael_demo', 
        name='raphael_demo'),   
    url(r'^charts/rtest', 'influence.views.rtest', 
        name='rtest.html'),   


    # make sure this goes after the more specific urls or it will
    # match before the others get hit.
    url(r'^', 'influence.views.index', name='index'),                       
)
