from django.conf.urls.defaults import *

urlpatterns = patterns('brisket.ecards.views',
    url(r'^$', 'choose_card'),
    url('^thanks/$', 'thanks'),
    url('^ecard/(?P<card>\w+)/', 'ecard'),
    url('^(?P<card>\w+)/', 'send_card'),
)