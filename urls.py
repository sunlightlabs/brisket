from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # evil url for media. 
    url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url('^contact/$', 'brisket.views.contact', name='contact_form'),
    url('^about/$', TemplateView.as_view(template_name='about.html')),
    url('^deprecation/$', TemplateView.as_view(template_name='deprecation.html')),
    url('^fixed-fortunes/', include('fortune_blank_hundred.urls')),
#    (r'^admin/', include(admin.site.urls)),
#    (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(admin.__file__) + '/media'}),
    # everything else goes to influence
    url(r'^', include('brisket.influence.urls')),
)

if settings.DEBUG:
    from django.shortcuts import render_to_response
    
    def design_view(request, path):
        return render_to_response('design/%s' % path)
        
    urlpatterns += patterns('',
        url('design/(?P<path>.*)$', design_view),
    )

handler404 = 'brisket.views.page_not_found'
handler500 = 'brisket.views.server_error'
