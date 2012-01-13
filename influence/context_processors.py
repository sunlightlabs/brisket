from influence.forms import SearchForm
from django.conf import settings

def custom_context(request):
    return {
        'search_form': SearchForm(),
        'API_KEY': getattr(settings, 'CLIENT_API_KEY', settings.API_KEY),
        'AGGREGATES_API_BASE_URL': getattr(settings, 'CLIENT_AGGREGATES_API_BASE_URL', settings.AGGREGATES_API_BASE_URL)
    }