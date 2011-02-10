from django.conf.urls.defaults import *

urlpatterns = patterns('brisket.ecards.views',
    url(r'^$', 'send_card'),
    url('^thanks/$', 'thanks'),
)