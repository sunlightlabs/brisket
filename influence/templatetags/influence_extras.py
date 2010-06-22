from django.template.defaultfilters import stringfilter
from django import template
from influence import helpers

register = template.Library()

@register.filter(name='standardize_politician_name')
@stringfilter
def standardize_politician_name_filter(name):
    return helpers.standardize_politician_name(name)

