from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse

QS_PARAM = getattr(settings, 'APIKEY_QS_PARAM', 'key')
HTTP_HEADER = getattr(settings, 'APIKEY_HTTP_HEADER', 'HTTP_X_API_KEY')

class KeyAuthentication(object):
    
    def is_authenticated(self, request):
        
        key = request.GET.get(QS_PARAM, None) or request.META.get(HTTP_HEADER, None)
        
        if key is not None:
            
            try:
                
                user = User.objects.get(api_keys__value=key)
                request.user = user
                return True
                
            except User.DoesNotExist:
                pass # we're okay with that, you just can't use the API
        
        return False
        
        
    
    def challenge(self):
        return HttpResponse('You need a key', content_type='text/plain')