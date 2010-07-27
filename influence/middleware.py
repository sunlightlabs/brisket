import re
from influence.models import PageRequest

class RequestLoggingMiddleware():

    def process_request(self, request):
        if not self.should_log(request):
            return None

        if not request.META.has_key('REMOTE_ADDR'):
            request.META['REMOTE_ADDR'] = request.META.get('HTTP_X_REAL_IP', '1.1.1.1')

        page_request = PageRequest.objects.create(
            ip_address    = request.META.get('REMOTE_ADDR'),
            path          = request.path,
            query_params  = request.META.get('QUERY_STRING'),
            referring_url = request.META.get('HTTP_REFERER'),
            user_agent    = request.META.get('USER_AGENT'),
        )

        request.session['page_request_id'] = page_request.id


    def process_response(self, request, response):
        if not self.should_log(request):
            return response

        page_request = self.get_existing_page_request(request)

        if self.page_request_is_valid(request, page_request):
            # saving will update the responded_at timestamp
            page_request.save()

        return response


    def process_exception(self, request, exception):
        if not self.should_log(request):
            raise exception

        page_request = self.get_existing_page_request(request)

        if self.page_request_is_valid(request, page_request):
            page_request.was_exception = True
            page_request.save()

        raise exception


    def get_existing_page_request(self, request):
        if request.session.get('page_request_id'):
            page_request = PageRequest.objects.get(id=request.session['page_request_id'])

            if page_request:
                return page_request


    def page_request_is_valid(self, request, page_request):
        return \
            page_request \
            and page_request.ip_address == request.META.get('REMOTE_ADDR') \
            and page_request.path == request.path \
            and page_request.query_params == request.META.get('QUERY_STRING')


    def should_log(self, request):
        return not re.match(r'(^/media|.*\.ico$)', request.path)


