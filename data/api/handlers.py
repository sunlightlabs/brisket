from piston.handler import BaseHandler
from matchbox.models import Entity
from dcdata.contribution.models import Contribution
from dc_web.search.contributions import CONTRIBUTION_SCHEMA

class ContributionFilterHandler(BaseHandler):
    allowed_methods = ('GET',)
    exclude = ('id','import_reference')
    model = Contribution
    
    def read(self, request):
        params = request.GET.copy()
        if 'key' in params:
            del params['key']
        q = CONTRIBUTION_SCHEMA.extract_query(params)
        return Contribution.objects.filter(*q)[:3]

class EntityHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Entity
    
    def read(self, request, entity_id):
        return Entity.objects.get(pk=entity_id)