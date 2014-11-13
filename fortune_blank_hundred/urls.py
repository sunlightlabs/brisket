from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    # resource pages
    url(r'^$', FortuneIndexView.as_view(),
        name='fortune-index-view'),
    url(r'^methodology$', FortuneMethodologyView.as_view(),
        name='fortune-methodology-view'),
    url(r'^overview$', FortuneOverviewView.as_view(),
        name='fortune-overview-view'),
)
