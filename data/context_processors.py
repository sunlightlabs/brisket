from influence.forms import SearchForm
from django.conf import settings

def custom_context(request):
    out = {}
    if hasattr(request, 'urlconf') and request.urlconf == 'brisket.data.urls':
        # we're on data.X, so TD urls can be root-relative and IE urls need a full path
        out['IE_BASE_URL'] = getattr(settings, "IE_BASE_URL", "http://influenceexplorer.com/")
        out['DATA_BASE_URL'] = "/"
    else:
        # we're on IE, so it's the reverse
        out['IE_BASE_URL'] = "/"
        out['DATA_BASE_URL'] = getattr(settings, "DATA_BASE_URL", "http://data.influenceexplorer.com/")
    
    out['DATA_API_BASE_URL'] = getattr(settings, "DATA_API_BASE_URL", "http://transparencydata.com/data/")
    
    return out