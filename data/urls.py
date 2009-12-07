from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from registration.views import activate
from registration.views import register
from dc_web.public.forms import CustomRegistrationForm

admin.autodiscover()

# registration URLs
urlpatterns = patterns('',
    url(r'^accounts/register/$', register, {
            'form_class': CustomRegistrationForm,
            'backend': 'registration.backends.default.DefaultBackend'
        }, name='registration_register'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/1.0/', include('dc_web.api.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^', include('dc_web.public.urls')),
)

if (settings.DEBUG):  
    urlpatterns += patterns('',  
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
    )