from django.conf.urls.defaults import *
from piston.resource import Resource
from dc_web.api.handlers import ContributionFilterHandler, EntityHandler

contributionfilter_handler = Resource(ContributionFilterHandler)
entity_handler = Resource(EntityHandler)

urlpatterns = patterns('',
    url(r'^contributions.(?P<emitter_format>.+)$', contributionfilter_handler),
    url(r'^entities/(?P<entity_id>\w+)(?P<emitter_format>.+)$', entity_handler),
)

