from django.conf.urls.defaults import *
from piston.emitters import Emitter
from piston.resource import Resource
from dc_web.api.handlers import ContributionFilterHandler, EntityHandler
from dc_web.api.auth import KeyAuthentication
from dc_web.api.emitters import CSVEmitter

Emitter.register('csv', CSVEmitter, 'text/csv')

ad = { 'authentication': KeyAuthentication() }

contributionfilter_handler = Resource(ContributionFilterHandler, **ad)
entity_handler = Resource(EntityHandler, **ad)

urlpatterns = patterns('',
    url(r'^contributions.(?P<emitter_format>.+)$', contributionfilter_handler),
    url(r'^entities/(?P<entity_id>\w+)(?P<emitter_format>.+)$', entity_handler),
)

