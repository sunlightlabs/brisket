class DataRedirectMiddleware(object):
    def process_request(self, request):
        if request.META['HTTP_HOST'].startswith('data.') or request.META['SERVER_PORT'] == '8100':
            request.urlconf = 'data.urls'
            request.dryrub_url_mode = 'data_relative'
        else:
            request.dryrub_url_mode = 'brisket_relative'
        return None
