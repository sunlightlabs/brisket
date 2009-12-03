from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^auth/login/$', 'login', name="login"),
    url(r'^auth/logout/$', 'logout_then_login', name="logout"),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/1.0/', include('dc_web.api.urls')),
    url(r'^', include('dc_web.public.urls')),
)

if (settings.DEBUG):  
    urlpatterns += patterns('',  
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
    )