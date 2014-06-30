from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    # resource pages
    url(r'^$', FortuneIndexView.as_view(), name='fortune-index-view'),
)
