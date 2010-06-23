import re
import string

def standardize_politician_name(name):
    no_party = strip_party(name)
    proper_case = convert_case(no_party)
    right_order = convert_to_standard_order(proper_case)

    return right_order

def strip_party(name):
    return re.sub(r'\s*\(\w+\)\s*$', '', name)

def convert_case(name):
    if not re.search(r'[A-Z][a-z]', name):
        return string.capwords(name)
    else:
        return name

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
