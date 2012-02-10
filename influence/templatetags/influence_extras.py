from django import template
from django.template.defaultfilters import stringfilter
from BeautifulSoup import BeautifulSoup
from name_cleaver import PoliticianNameCleaver, IndividualNameCleaver, \
        OrganizationNameCleaver
from influence.helpers import standardize_name

register = template.Library()

SUNLIGHT_STAFF_BASE_URI = "http://sunlightfoundation.com/people/"

@register.filter(name='standardize_politician_name')
@stringfilter
def standardize_politician_name_filter(name):
    return str(PoliticianNameCleaver(name).parse())

@register.filter(name='standardize_individual_name')
@stringfilter
def standardize_individual_name_filter(name):
    return str(IndividualNameCleaver(name).parse())

@register.filter(name='standardize_organization_name')
@stringfilter
def standardize_organization_name_filter(name):
    return str(OrganizationNameCleaver(name).parse())

@register.filter(name='standardize_industry_name')
@stringfilter
def standardize_industry_name_filter(name):
    return str(OrganizationNameCleaver(name).parse())

@register.filter(name='standardize_name')
@stringfilter
def standardize_name_filter(name, type):
    return standardize_name(name, type)


seat_labels = {'federal:senate': 'US Senate',
               'federal:house': 'US House',
               'federal:president': 'President',
               'state:upper': 'State Upper Chamber',
               'state:lower': 'State Lower Chamber',
               'state:governor': 'Governor',
               'state:ltgovernor': 'Lt. Governor',
               'state:judicial': 'State Judiciary',
               'state:office': 'Other State Office'
               }

seat_adjectives = {'federal:senate': 'Senate',
               'federal:house': 'House',
               'federal:president': 'Presidential',
               'state:upper': 'State Upper Chamber',
               'state:lower': 'State Lower Chamber',
               'state:governor': 'Gubernatorial',
               'state:ltgovernor': 'Lt. Governor',
               'state:judicial': 'State Judiciary',
               'state:office': 'Other State Office'
               }

@register.filter(name='seat_label')
@stringfilter
def seat_label_filter(raw):
    return seat_labels.get(raw, raw)

@register.filter(name='seat_adjective')
@stringfilter
def seat_adjective_filter(raw):
    return seat_adjectives.get(raw, raw)


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

@register.filter(name='comma')
def comma_filter(loop):
    out = ''
    total = loop['revcounter'] + loop['counter0']
    if total > 2 and not loop['last']:
        out = ', '
        if loop['counter0'] == total - 2:
            out = out + 'and '
    return out

@register.filter(name='colon')
def colon_filter(loop, desc):
    if loop['last'] and desc:
        return ':'
    return ''

@register.filter(name='earpunc')
def earpunc_filter(loop, desc):
    return comma_filter(loop) + colon_filter(loop, desc)

@register.filter(name='nonempty_lines')
def nonempty_lines_filter(text):
    lines = [line.strip() for line in text.split('\n')]
    return [line for line in lines if line]

@register.filter(name='pretty_list')
def pretty_list_filter(l):
    if len(l) < 3:
        return ' and '.join(l)
    else:
        return '%s and %s' % (', '.join(l[:-1]), l[-1])

@register.filter
@stringfilter
def sunlight_author_uri(value):
    value = value.lower().split(' ')
    if len(value) > 1:
        shortname = "%s%s"%(value[0][:1],value[-1])
    else:
        shortname = value[0]
    return "%s%s"%(SUNLIGHT_STAFF_BASE_URI, shortname)

@register.filter(name='first_paragraph')
@stringfilter
def first_paragraph_filter(t):
    b = BeautifulSoup(t)
    paras = b.findChildren('p')
    if paras:
        return unicode(paras[0])
    else:
        return t
