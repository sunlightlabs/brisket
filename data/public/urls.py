from django.conf.urls.defaults import *

urlpatterns = patterns('dc_web.public.views',
    url(r'^account/$', 'account_index', name="dcweb_account_index"),
    url(r'^account/create/$', 'account_create', name="dcweb_account_create"),
    url(r'^$', 'index', name="dcweb_index"),
)
