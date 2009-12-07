from django.conf.urls.defaults import *

urlpatterns = patterns('dc_web.public.views',
    url(r'^api/$', 'api_index', name="api_index"),
    url(r'^bulk/$', 'bulk_index', name="bulk_index"),
    url(r'^$', 'index', name="index"),
)
