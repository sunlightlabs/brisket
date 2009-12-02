
from datetime import date

from django.db.models.query_utils import Q


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
    def __init__(self, param_name, *operators):
        self._param_name = param_name
        
        self._name_to_op = dict()
        for op in [op for op in operators]:
            self._name_to_op[op.get_name()] = op
            
    def get_op_names(self):
        return self._name_to_op.keys()
    
    def get_op(self, name):
        return self._name_to_op[name]
    
    def get_name(self):
        return self._param_name
    
        
class Schema(object):
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
    return Q(datestamp__range=(_date_from_string(first), _date_from_string(second)))

def _contributor_in_generator(*entities):    
    return Q(contributor_entity__in=entities) | Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities)
    
def _recipient_in_generator(entities):
    return Q(recipient_entity__in=entities) | Q(committee_entity__in=entities)    

def _entity_in_generator(entities):
    return _contributor_in_generator(entities) | _recipient_in_generator(entities)

def _amount_less_than_generator(amount):
    return Q(amount__lte=int(amount))

def _amount_greater_than_generator(amount):
    return Q(amount__gte=int(amount))

def _amount_between_generator(lower, upper):
    return Q(amount__range=(int(lower), int(upper)))

def _cycle_equals_generator(cycle):
    return Q(cycle=int(cycle))


ENTITY_TYPE = 'entities'
DATE_TYPE = 'date'
AMOUNT_TYPE = 'amount'
STATE_TYPE = 'state'
CYCLE_TYPE = 'cycle'

IN_OP = 'in'
EQUALS_OP = '='
LESS_THAN_OP = '<'
GREATER_THAN_OP = '>'
BETWEEN_OP = '><'

STATE_FIELD = 'state'
DATE_FIELD = 'date'
CONTRIBUTOR_FIELD ='contributor'
RECIPIENT_FIELD = 'recipient'
ENTITY_FIELD = 'entity'
AMOUNT_FIELD = 'amount'
CYCLE_FIELD = 'cycle'


CONTRIBUTION_SCHEMA = Schema(Field(STATE_FIELD,
                                   Operator(EQUALS_OP, _state_equals_generator, [STATE_TYPE])),
                             Field(DATE_FIELD,
                                   Operator(LESS_THAN_OP, _date_before_generator, [DATE_TYPE]),
                                   Operator(GREATER_THAN_OP, _date_after_generator, [DATE_TYPE]),
                                   Operator(BETWEEN_OP, _date_between_generator, [DATE_TYPE, DATE_TYPE])),
                             Field(CONTRIBUTOR_FIELD,
                                   Operator(IN_OP, _contributor_in_generator, [ENTITY_TYPE])),
                             Field(RECIPIENT_FIELD,
                                   Operator(IN_OP, _recipient_in_generator, [ENTITY_TYPE])),
                             Field(ENTITY_FIELD,
                                   Operator(IN_OP, _entity_in_generator, [ENTITY_TYPE])),
                             Field(AMOUNT_FIELD,
                                   Operator(LESS_THAN_OP, _amount_less_than_generator, [AMOUNT_TYPE]),
                                   Operator(GREATER_THAN_OP, _amount_greater_than_generator, [AMOUNT_TYPE]),
                                   Operator(BETWEEN_OP, _amount_between_generator, [AMOUNT_TYPE, AMOUNT_TYPE])),
                             Field(CYCLE_FIELD,
                                   Operator(EQUALS_OP, _cycle_equals_generator, [CYCLE_TYPE])))


##### Parsing of HTTP Requests #####

VALUE_DELIMITER = '|'

def extract_query(request):
    def extract_clause(field_name, value):
        value_components = value.split(VALUE_DELIMITER)
        op_name = value_components[0]
        args = value_components[1:]
        return CONTRIBUTION_SCHEMA.get_query_clause(field_name, op_name, *args)
    
    return [extract_clause(name, value) for (name, value) in request.items()]


