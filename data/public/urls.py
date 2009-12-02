from django.conf.urls.defaults import *

urlpatterns = patterns('dc_web.public.views',
    url(r'^$', 'index', name="dcweb_index"),
)
