class DataRedirectMiddleware(object):
    def process_request(self, request):
        if request.META['HTTP_HOST'].startswith('data.') or request.META['SERVER_PORT'] == '8100':
            request.urlconf = 'brisket.data.urls'
        return None
