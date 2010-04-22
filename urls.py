from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # evil url for media. 
    url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^experimental/', include('brisket.experimental.urls')),
    # everything else goes to influence
    url(r'^', include('brisket.influence.urls')),
)
