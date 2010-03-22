RETURN_ENTITIES_KEY = 'api_return_entities'

class APIMiddleware(object):
    def process_request(self, request):
        use_entities = request.GET.get('return_entities', None)
        if use_entities == '1':
            request.session[RETURN_ENTITIES_KEY] = True
        elif use_entities == '0':
            request.session[RETURN_ENTITIES_KEY] = False
            