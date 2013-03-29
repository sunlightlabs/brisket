class DataRedirectMiddleware(object):
    def process_request(self, request):
        if request.META['HTTP_HOST'].startswith('data.') or request.META['SERVER_PORT'] == '8002':
            request.urlconf = 'data.urls'
        return None
