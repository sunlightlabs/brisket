from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
SUNLIGHT_STAFF_BASE_URI = "http://sunlightfoundation.com/people/"
@register.filter
@stringfilter
def sunlight_author_uri(value):
    value = value.lower().split(' ')
    return SUNLIGHT_STAFF_BASE_URI,value[0][:1],value[1]
    
    