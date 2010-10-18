from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('brisket.postcards.views',
    url(r'^$', direct_to_template, {'template': 'postcards/landing.html'}),
    url(r'^/order$', direct_to_template, {'template': 'postcards/order.html'}),
#    url(r'^/confirm$', 'confirm'),
#    url(r'^/thanks$', 'thanks'),
#    url(r'^/hook$', 'hook'),
)
