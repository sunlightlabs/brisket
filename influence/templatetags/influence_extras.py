from django.template.defaultfilters import stringfilter
from django import template
from influence import helpers

register = template.Library()

@register.filter(name='standardize_politician_name')
@stringfilter
def standardize_politician_name_filter(name):
    return helpers.standardize_politician_name(name)



seat_labels = {'federal:senate': 'Senate',
               'federal:house': 'House',
               'federal:president': 'President',
               'state:upper': 'State Upper Chamber',
               'state:lower': 'State Lower Chamber',
               'state:governor': 'State Governor',
               'state:judicial': 'State Judiciary',
               'state:office': 'Other State Office'
               }

@register.filter(name='seat_label')
@stringfilter
def seat_label_filter(raw):
    return seat_labels.get(raw, raw)