from django.conf.urls.defaults import *

urlpatterns = patterns('brisket.ecards.views',
    url(r'^$', 'choose_card'),
    url('^thanks/$', 'thanks'),
    url('^signup/$', 'signup_simple'),
    url('^ecard/(?P<card>\w+)/(?P<message_id>\d+)/(?P<message_hash>\w+)/$', 'ecard'),
    url('^ecard/(?P<card>\w+)/$', 'ecard'),
    url('^(?P<card>\w+)/$', 'send_card'),
)