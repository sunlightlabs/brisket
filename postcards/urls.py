from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('brisket.postcards.views',
    url(r'^$', direct_to_template, {'template': 'postcards/landing.html'}),
    url(r'^/order$', 'order'),
    url(r'^/thumbnail/(?P<type>\w+)/(?P<id>[\w\-]+)$', 'thumbnail'),
    url(r'^/confirm/(?P<id>\d+)/(?P<hash>\w+)$', 'confirm'),
    url(r'^/text_preview/(?P<id>\d+)/(?P<hash>\w+)$', 'preview'),
#    url(r'^/thanks$', 'thanks'),
#    url(r'^/hook$', 'hook'),
)
