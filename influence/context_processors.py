from influence.forms import SearchForm
from django.conf import settings
import urlparse

def custom_context(request):
    return {
        'search_form': SearchForm(),
        'API_KEY': getattr(settings, 'CLIENT_API_KEY', settings.API_KEY),
        'AGGREGATES_API_BASE_URL': getattr(settings, 'CLIENT_AGGREGATES_API_BASE_URL', settings.AGGREGATES_API_BASE_URL),
        'DOCKETWRENCH_URL': getattr(settings, 'DOCKETWRENCH_URL', 'http://docketwrench.sunlightfoundation.com'),
        'FIRST_VIEW': urlparse.urlparse(request.META.get('HTTP_REFERER', '')).netloc != request.META.get('HTTP_HOST', ''),
        'CHART_FALLBACK_URL': getattr(settings, 'CHART_FALLBACK_URL', '/chart/'),
    }