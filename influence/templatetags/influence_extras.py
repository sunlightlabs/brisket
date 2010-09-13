from django.template.defaultfilters import stringfilter
from django import template
from influence import helpers

register = template.Library()

@register.filter(name='standardize_politician_name')
@stringfilter
def standardize_politician_name_filter(name):
    return helpers.standardize_politician_name(name)

@register.filter(name='standardize_individual_name')
@stringfilter
def standardize_individual_name_filter(name):
    return helpers.standardize_individual_name(name)

@register.filter(name='standardize_organization_name')
@stringfilter
def standardize_organization_name_filter(name):
    return helpers.standardize_organization_name(name)


seat_labels = {'federal:senate': 'US Senate',
               'federal:house': 'US House',
               'federal:president': 'President',
               'state:upper': 'State Upper Chamber',
               'state:lower': 'State Lower Chamber',
               'state:governor': 'Governor',
               'state:judicial': 'State Judiciary',
               'state:office': 'Other State Office'
               }

@register.filter(name='seat_label')
@stringfilter
def seat_label_filter(raw):
    return seat_labels.get(raw, raw)


seat_titles = {'federal:senate': 'Sen.',
               'federal:house': 'Rep.',
               'federal:president': 'Pres.',
               'state:governor': 'Gov.',
}

@register.filter(name='seat_title')
@stringfilter
def seat_title_filter(person, seat):
    if seat and seat in seat_titles:
        return '%s %s' % (seat_titles.get(seat), person)
    else:
        return person


@register.filter(name='pretty_cycle')
@stringfilter
def pretty_cycle_filter(cycle):
    if str(cycle) == '-1':
        return ''
    else:
        return '?cycle=%s' % cycle
