import re
import string
from name_cleaver import PoliticianNameCleaver


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
    name = name.strip()
    name = convert_case(name)

    if re.match(r'(?i)^\w*PAC$', name):
        name = name.upper() # if there's only one word that ends in PAC, make the whole thing uppercase
    else:
        name = re.sub(r'(?i)\bpac\b', 'PAC', name) # otherwise just uppercase the PAC part

    return name

def standardize_industry_name(name):
    name = convert_case(name)
    name = name.strip()
    name = re.sub(r'/([a-z])', lambda s: s.group().upper(), name)
    name = re.sub(r'-([a-z])', lambda s: s.group().upper(), name)

    return name

_standardizers = {
    'politician': lambda n: PoliticianNameCleaver(n).parse(),
    'individual': standardize_individual_name,
    'industry': standardize_industry_name,
    'organization': standardize_organization_name,
}

def standardize_name(name, type):
    return _standardizers[type](name)

def separate_affixes(name):
    # this should match both honorifics (mr/mrs/ms) and jr/sr/II/III
    matches = re.search(r'^\s*(?P<name>.*)\b((?P<honorific>m[rs]s?.?)|(?P<suffix>([js]r|I{2,})))[.,]?\s*$', name, re.IGNORECASE)
    if matches:
        return matches.group('name', 'honorific', 'suffix')
    else:
        return name, None, None

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
    matches = re.search(r'(?i)\b(?P<mc>ma?c)(?P<first_letter>\w)', name)
    if matches:
        mc = matches.group('mc')
        first_letter = matches.group('first_letter')
        return re.sub(mc + first_letter, mc.title() + first_letter.upper(), name)
    else:
        return name

def is_mixed_case(name):
    return re.search(r'[A-Z][a-z]', name)

def convert_name_to_first_last(name):
    split = name.split(',')
    if len(split) == 1: return split[0]

    trimmed_split = [ x.strip() for x in split ]

    trimmed_split.reverse()
    return ' '.join(trimmed_split)

