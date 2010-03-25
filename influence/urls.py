from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^search', 'influence.views.search', name='search'),                       
    url(r'^', 'influence.views.index', name='index'),                       
)
