
from datetime import date

from django.db.models.query_utils import Q


##### Generic Data Model #####

ARGUMENT_TYPES = ('entities', 'date', 'amount', 'state', 'cycle')

class Operator(object):
    def __init__(self, param_name, generator, args):
        self._param_name = param_name
        self._generator = generator
        self._args = args
        
    def get_arg_types(self):
        return self._args
    
    def get_name(self):
        return self._param_name
    
    def apply(self, *args):
        return self._generator(*args)


class Field(object):
    def __init__(self, param_name, **kwargs):
        self._param_name = param_name
        self._before_op = kwargs.get('before_op', None)
        self._after_op = kwargs.get('after_op', None)
        self._between_op = kwargs.get('between_op', None)
        self._equals_op = kwargs.get('equals_op', None)
        self._in_op = kwargs.get('in_op', None)
        
        self._name_to_op = dict()
        for op in [op for op in [self._before_op, self._after_op, self._between_op, self._equals_op, self._in_op] if op]:
            self._name_to_op[op.get_name()] = op
            
    def get_op_names(self):
        return self._name_to_op.keys()
    
    def get_op(self, name):
        return self._name_to_op[name]
    
    def get_name(self):
        return self._param_name
    
        
class Syntax(object):
    def __init__(self, *search_fields):
        self._name_to_field = dict()
        for search_field in search_fields:
            self._name_to_field[search_field.get_name()] = search_field

    def get_field_names(self):
        return self._name_to_field.keys()
    
    def get_field(self, name):
        return self._name_to_field[name]
    
    def get_query_clause(self, field_name, op_name, *values):
        return self.get_field(field_name).get_op(op_name).apply(*values)
        


 
##### Specific Queries #####

def _date_from_string(string_val):
    (year, month, day) = string_val.split('-')
    return date(int(year), int(month), int(day))

def _state_equals_generator(state):
    return Q(state=state)

def _date_before_generator(date):
    return Q(datestamp__lte=_date_from_string(date))

def _date_after_generator(date):
    return Q(datestamp__gte=_date_from_string(date))

def _date_between_generator(first, second):
    return Q(datestamp__rang=(_date_from_string(first), _date_from_string(second)))

def _contributor_in_generator(*entities):    
    return Q(contributor_entity__in=entities) | Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities)
    
def _recipient_in_generator(entities):
    return Q(recipient_entity__in=entities) | Q(committee_entity__in=entities)    



STATE_FIELD = Field('state',
                    equals_op = Operator('=',
                                         _state_equals_generator,
                                         ['state']))

DATE_FIELD = Field('date',
                     before_op = Operator('<',
                                          _date_before_generator,
                                          ['date']),
                     after_op = Operator('>',
                                         _date_after_generator,
                                         ['date']),
                     between_op = Operator('><',
                                           _date_between_generator,
                                           ['date', 'date']))
    
CONTRIBUTOR_FIELD = Field('contributor',
                           in_op = Operator('in',
                                            _contributor_in_generator,
                                            ['entities']))
    
RECIPIENT_FIELD = Field('recipient',
                         in_op = Operator('in',
                                          _recipient_in_generator,
                                          ['entities']))

SYNTAX = Syntax(STATE_FIELD, DATE_FIELD, CONTRIBUTOR_FIELD, RECIPIENT_FIELD)



##### Parsing of HTTP Requests #####

VALUE_DELIMITER = '|'

def extract_query(request):
    def extract_clause(field_name, value):
        value_components = value.split(VALUE_DELIMITER)
        op_name = value_components[0]
        args = value_components[1:]
        return SYNTAX.get_query_clause(field_name, op_name, *args)
    
    return [extract_clause(name, value) for (name, value) in request.items()]