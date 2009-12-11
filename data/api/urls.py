from django.conf.urls.defaults import *
from piston.emitters import Emitter
from piston.resource import Resource
from dc_web.api.handlers import ContributionFilterHandler, EntityHandler, EntityFilterHandler
from dc_web.api.auth import KeyAuthentication
from dc_web.api.emitters import StreamingLoggingCSVEmitter, StreamingLoggingJSONEmitter

Emitter.register('csv', StreamingLoggingCSVEmitter, 'text/csv')
Emitter.register('json', StreamingLoggingJSONEmitter, 'application/json')
Emitter.unregister('django')
Emitter.unregister('pickle')
Emitter.unregister('xml')
Emitter.unregister('yaml')

ad = { 'authentication': KeyAuthentication() }

contributionfilter_handler = Resource(ContributionFilterHandler, **ad)
entity_handler = Resource(EntityHandler, **ad)
entityfilter_handler = Resource(EntityFilterHandler, **ad)

urlpatterns = patterns('',
    url(r'^contributions.(?P<emitter_format>.+)$', contributionfilter_handler, name='api_contributions_filter'),
    url(r'^entities/(?P<entity_id>\w+).(?P<emitter_format>.+)$', entity_handler, name='api_entities'),
    url(r'^entities.(?P<emitter_format>.+)$', entityfilter_handler, name='api_entities_filter'),
)

