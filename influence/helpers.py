import re, string, datetime
import api
from util import catcodes
from django.template.defaultfilters import slugify
from django.http import Http404

def standardize_politician_name_with_metadata(name, party, state):
    party_state = "-".join([x for x in [party, state] if x]) # because presidential candidates are listed without a state
    name = "{0} ({1})".format(standardize_politician_name(name), party_state)

    return name

def standardize_politician_name(name):
    name = strip_party(name)
    name = convert_to_standard_order(name)

    return convert_case(name)

def standardize_individual_name(name):
    name, honorific, suffix = separate_affixes(name)

    name = convert_name_to_first_last(name)
    name = ' '.join([x for x in [
        honorific if honorific and honorific.lower() == 'mrs' else None,
        name,
        suffix
    ] if x])
    name = re.sub(r'\d{2,}\s*$', '', name) # strip any trailing numbers
    name = re.sub(r'^(?i)\s*mr\.?\s+', '', name) # strip leading 'Mr' if not caught by the other algorithm (e.g. the name was in first last format to begin with)

    return convert_case(name)

def standardize_organization_name(name):
    name = convert_case(name)
    name = name.strip()

    if re.match(r'(?i)^\w*PAC$', name):
        name = name.upper() # if there's only one word that ends in PAC, make the whole thing uppercase
    else:
        name = re.sub(r'(?i)\bpac\b', 'PAC', name) # otherwise just uppercase the PAC part

    return name

def standardize_industry_name(name):
    name = convert_case(name)
    name = name.strip()
    
    return name

def separate_affixes(name):
    # this should match both honorifics (mr/mrs/ms) and jr/sr/II/III
    matches = re.search(r'^\s*(?P<name>.*)\b((?P<honorific>m[rs]s?.?)|(?P<suffix>([js]r|I{2,})))[.,]?\s*$', name, re.IGNORECASE)
    if matches:
        return matches.group('name', 'honorific', 'suffix')
    else:
        return name, None, None

def strip_party(name):
    return re.sub(r'\s*\(\w+\)\s*$', '', name)

def convert_case(name):
    name = name if is_mixed_case(name) else string.capwords(name)
    name = uppercase_roman_numeral_suffix(name)
    return uppercase_the_scots(name)

def uppercase_roman_numeral_suffix(name):
    matches = re.search(r'(?i)(?P<suffix>\b[ivx]+)$', name)
    if matches:
        suffix = matches.group('suffix')
        return re.sub(suffix, suffix.upper(), name)
    else:
        return name

def uppercase_the_scots(name):
    matches = re.search(r'(?i) (?P<mc>ma?c)(?P<first_letter>\w)', name)
    if matches:
        mc = matches.group('mc')
        first_letter = matches.group('first_letter')
        return re.sub(mc + first_letter, mc.title() + first_letter.upper(), name)
    else:
        return name

def is_mixed_case(name):
    return re.search(r'[A-Z][a-z]', name)

def convert_to_standard_order(name):
    if '&' in name:
        return convert_running_mates(name)
    else:
        return convert_name_to_first_last(name)

def convert_name_to_first_last(name):
    split = name.split(',')
    if len(split) == 1: return split[0]

    trimmed_split = [ x.strip() for x in split ]

    trimmed_split.reverse()
    return ' '.join(trimmed_split)

def convert_running_mates(name):
    mates = name.split('&')
    fixed_mates = []
    for name in mates:
        fixed_mates.append(convert_name_to_first_last(name))

    return ' & '.join(fixed_mates).strip()


# lobbying
def lobbying_by_industry(lobbying_data):
    ''' aggregates lobbying spending by industry'''
    amt_by_industry = {}
    for transaction in lobbying_data:
        industry = transaction['client_category']
        amount = transaction['amount']
        amt_by_industry[industry] = amt_by_industry.get(industry, 0) + int(float(amount))
    # sort into a list of (sector_code, amt) tuples
    z = zip(amt_by_industry.keys(), amt_by_industry.values())
    z.sort(_tuple_cmp, reverse=True)
    # add in the industry and area names
    # return tuples now contain (industry_code, industry_name, industry_area, amt)
    annotated = []
    for item in z:
        code = item[0]
        industry = catcodes.industry_area[item[0].upper()][0]
        sub_industry = catcodes.industry_area[item[0].upper()][1]
        amount = item[1]
        annotated.append((code, industry, sub_industry, amount))
    return annotated

def lobbying_by_customer(lobbying_data):
    amt_by_customer = {}
    for transaction in lobbying_data:
        #if not transaction['registrant_is_firm']:
        #    continue
        customer = transaction['client_name']
        amount = transaction['amount']
        amt_by_customer[customer] = amt_by_customer.get(customer, 0) + int(float(amount))
    # sort and return as list of (firm, amt) tuples
    z = zip(amt_by_customer.keys(), amt_by_customer.values())
    z.sort(_tuple_cmp, reverse=True)
    return z


def lobbying_by_firm(lobbying_data):
    amt_by_firm = {}
    for transaction in lobbying_data:
        #if not transaction['registrant_is_firm']:
        #    continue
        firm = transaction['registrant_name']
        amount = transaction['amount']
        amt_by_firm[firm] = amt_by_firm.get(firm, 0) + int(float(amount))
    # sort and return as list of (firm, amt) tuples
    z = zip(amt_by_firm.keys(), amt_by_firm.values())
    z.sort(_tuple_cmp, reverse=True) # stupid in place sorting
    return z

# random util/helper functions

def tuple_cmp(t1, t2):
    ''' a cmp function for sort(), to sort tuples by increasing value
    of the tuple's 2nd item (index 1)'''
    if t1[1] < t2[1]:
        return -1
    if t1[1] > t2[1]:
        return 1
    else: return 0

def bar_validate(data):
    ''' take a dict formatted for submission to the barchart
     generation function, and make sure there's data worth displaying.
     if so, return the original data. if not, return false.'''

    positive_data = [d for d in data if int(float(d['value'])) > 0]
    data = positive_data
    # if all the data is 0 or if the list with only positive data is
    # empty, return false
    if sum([int(float(record['value'])) for record in data]) == 0:
        return []
    else:
        return data

def pie_validate(data):
    ''' take a dict formatted for submission to the piechart
     generation function, and make sure there's data worth displaying.
     if so, return the original data. if not, return false.'''

    positive = {}
    for k,v in data.iteritems():
        if int(float(v)) != 0:
            positive[k] = v
    if len(positive) == 0:
        return []
    else:
        return positive

def barchart_href(record, cycle, entity_type):
    if record.get('recipient_entity', None):
            return str("/%s/%s/%s%s" % (entity_type, slugify(record['recipient_name']),
                                               record['recipient_entity'], "?cycle=" + cycle if cycle != "-1" else ""))
    elif record.get('id', None):
        if record['id']:
            return str("/%s/%s/%s%s" % (entity_type, slugify(record['name']),
                                               record['id'], "?cycle=" + cycle if cycle != "-1" else ""))
    return ''

def generate_label(string):
    ''' truncate names longer than max_length '''
    max_length = 34
    return string[:max_length] + (lambda x, l: (len(x)>l and "...")
                                   or "")(string, max_length)

def get_metadata(entity_id, cycle, entity_type):
    data = {}
    cycle_str = unicode(cycle)

    # check the metadata to see which of the fields are present. this
    # determines which sections to display on the entity page.
    section_indicators = {\
        'individual':   {'contributions': ['contributor_amount'], 'lobbying': ['lobbying_count']},\
        'organization': {'contributions': ['contributor_amount'], 'lobbying': ['lobbying_count']},\
        'industry': {'contributions': ['contributor_amount'], 'lobbying': ['lobbying_count']},\
        'politician':   {'contributions': ['recipient_amount']}\
    }

    entity_info = api.entity_metadata(entity_id, cycle)

    # check which types of data are available about this entity
    for data_type, indicators in section_indicators[entity_type].iteritems():
        if (entity_info['totals'].get(cycle_str, False) and
            [True for ind in indicators if entity_info['totals'][cycle_str][ind] ]):
            data[data_type] = True
        else:
            data[data_type] = False

    data['available_cycles'] = entity_info['totals'].keys()
    # discard the info from cycles that are not the current one
    if entity_info['totals'].get(cycle, None):
        entity_info['totals'] = entity_info['totals'][cycle_str]
    data['entity_info'] = entity_info

    return data

def months_into_cycle_for_date(date, cycle):
    end_of_cycle = datetime.datetime.strptime("{0}1231".format(cycle), "%Y%m%d").date()
    step = 24 - abs(((end_of_cycle.year - date.year) * 12) + end_of_cycle.month - date.month)
    return step


def check_entity(entity_info, cycle, entity_type):
    try:
        icycle = int(cycle)
    except:
        raise Http404
    if (icycle != -1 and (icycle < int(entity_info['career']['start']) or icycle > int(entity_info['career']['end']))) or entity_info['type'] != entity_type:
        raise Http404