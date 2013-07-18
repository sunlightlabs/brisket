from influence.forms import SearchForm
from django.conf import settings

def custom_context(request):
    out = {}
    dryrub_url_mode = getattr(request, 'dryrub_url_mode', 'all_absolute')
    if dryrub_url_mode == 'data_relative':
        # we're on data.X, so TD urls can be root-relative and IE urls need a full path
        out['IE_BASE_URL'] = getattr(settings, "IE_BASE_URL", "http://influenceexplorer.com/")
        out['DATA_BASE_URL'] = "/"
        
        # did we get here via redirect? if so, show doormat
        out['is_redirect'] = 'r' in request.GET
    elif dryrub_url_mode == 'brisket_relative':
        # we're on IE, so it's the reverse
        out['IE_BASE_URL'] = "/"
        out['DATA_BASE_URL'] = getattr(settings, "DATA_BASE_URL", "http://data.influenceexplorer.com/")

    else:
        # we're on a third-party property, so everything is absolute
        out['IE_BASE_URL'] = getattr(settings, "IE_BASE_URL", "http://influenceexplorer.com/")
        out['DATA_BASE_URL'] = getattr(settings, "DATA_BASE_URL", "http://data.influenceexplorer.com/")
    
    out['DATA_API_BASE_URL'] = getattr(settings, "DATA_API_BASE_URL", "http://transparencydata.com/data/")
    
    return out