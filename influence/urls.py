from django.conf.urls import patterns, url
from brisket.influence.sitemaps import sitemaps, index_wrapper, sitemap_wrapper

from django.views.generic import TemplateView

urlpatterns = patterns('brisket.influence.views',
    url(r'^$', 'index', name='index'),
)

urlpatterns += patterns('',
    # treat urls without the entity_id as search strings

    url(r'^contact/?$', TemplateView.as_view(template_name='contact.html')),

    url(r'^about/?$', TemplateView.as_view(template_name='about.html')),

    url(r'^about/methodology?$', TemplateView.as_view(template_name='methodology/methodology_landing.html')),

    url(r'^about/methodology/campaign_finance/?$', TemplateView.as_view(template_name='methodology/campaign_finance_methodology.html')),

    url(r'^about/methodology/lobbying/?$', TemplateView.as_view(template_name='methodology/lobbying_methodology.html')),

    url(r'^about/methodology/lobbyist_bundling/?$', TemplateView.as_view(template_name='methodology/lobbyist_bundling_methodology.html')),

    url(r'^about/methodology/fed_spending/?$', TemplateView.as_view(template_name='methodology/fed_spending_methodology.html')),

    url(r'^about/methodology/earmarks/?$', TemplateView.as_view(template_name='methodology/earmark_methodology.html')),

    url(r'^about/methodology/echo/?$', TemplateView.as_view(template_name='methodology/epa_echo_methodology.html')),
    url(r'^about/methodology/realtime-lobbying/registrations/?$', TemplateView.as_view(template_name='methodology/realtime_lobbying/registrations_methodology.html')),
    url(r'^about/methodology/realtime-lobbying/post-employment/?$', TemplateView.as_view(template_name='methodology/realtime_lobbying/post_employment_methodology.html')),

)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', index_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_wrapper, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
