import re
import string

def standardize_politician_name(name):
    no_party = strip_party(name)
    proper_case = convert_case(no_party)
    right_order = convert_name_to_first_last(proper_case)

    return right_order

def strip_party(name):
    return re.sub(r'\s*\(\w\)\s*$', '', name)

def convert_case(name):
    if not re.search(r'[A-Z][a-z]', name):
        return string.capwords(name)
    else:
        return name

def convert_name_to_first_last(name):
    split = name.split(',')
    if len(split) == 1: return split[0]

    split.reverse()
    return ' '.join(split).strip()

