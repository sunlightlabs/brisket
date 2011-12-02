from influence.forms import SearchForm
from django.conf import settings

def custom_context(request):
    return {
        'DATA_API_BASE_URL': getattr(settings, "DATA_API_BASE_URL", "http://transparencydata.com/data/")
    }