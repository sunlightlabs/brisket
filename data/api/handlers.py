from piston.handler import BaseHandler
from matchbox.models import Entity
from dcdata.contribution.models import Contribution
from dc_web.search.contributions import CONTRIBUTION_SCHEMA

class ContributionFilterHandler(BaseHandler):
    allowed_methods = ('GET',)
    exclude = ('id',)
    
    def read(self, request):
        q = CONTRIBUTION_SCHEMA.extract_query(request.GET)
        return Contribution.objects.filter(*q)[:1]

class EntityHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Entity
    
    def read(self, request, entity_id):
        return Entity.objects.get(pk=entity_id)