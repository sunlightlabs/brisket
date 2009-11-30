
from django.db.models.query_utils import Q



ARGUMENT_TYPES = ('entities', 'date', 'amount', 'state', 'cycle')


class Op(object):
    def __init__(self, param_name, generator, args):
        self.param_name = param_name
        self.generator = generator
        self.args = args
        
    def arity(self):
        return len(self.args)


class SearchField(object):
    def __init__(self, param_name, **kwargs):
        self.param_name = param_name
        self.before_op = kwargs.get('before_op', None)
        self.after_op = kwargs.get('after_op', None)
        self.between_op = kwargs.get('between_op', None)
        self.equals_op = kwargs.get('equals_op', None)
        self.in_op = kwargs.get('in_op', None)
        
        self.name_to_op = dict()
        for op in [op for op in [self.before_op, self.after_op, self.between_op, self.equals_op, self.in_op] if op]:
            self.name_to_op[op.param_name] = op
        
class QuerySyntax(object):
    def __init__(self, *search_fields):
        self.search_fields = search_fields
        self.name_to_field = dict()
        for search_field in search_fields:
            self.name_to_field[search_field.param_name] = search_field


def _date_before_generator(date):
    return Q(datestamp__lte=date)

def _date_after_generator(date):
    return Q(datestamp__gte=date)

def _date_between_generator(first, second):
    return Q(datestamp__rang=(first,second))

def _contributor_in_generator(*entities):    
    return Q(contributor_entity__in=entities) | Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities)
    
def _recipient_in_generator(entities):
    return Q(recipient_entity__in=entities) | Q(committee_entity__in=entities)    



##### architecture idea 1 #######
DATE_SEARCH = SearchField('date',
                         before_op = Op('<',
                                        _date_before_generator,
                                        ['date']),
                         after_op = Op('>',
                                       _date_after_generator,
                                       ['date']),
                         between_op = Op('><',
                                         _date_between_generator,
                                         ['date', 'date']))
    
CONTRIBUTOR_SEARCH = SearchField('contributor',
                                 in_op = Op('in',
                                            _contributor_in_generator,
                                            ['entities']))
    
RECIPIENT_SEARCH = SearchField('recipient',
                                 in_op = Op('in',
                                            _recipient_in_generator,
                                            ['entities']))

SEARCH_FIELDS = [DATE_SEARCH, CONTRIBUTOR_SEARCH, RECIPIENT_SEARCH]

##### architecture idea 2 #######
SEARCH_FIELDS = {'date': {'<': _date_before_generator,
                          '>': _date_after_generator,
                          '><': _date_between_generator},
                 'contributor': {'in': _contributor_in_generator},
                 'recipient': {'in': _recipient_in_generator}}


def build_query(ops_and_args):
    def apply(op_and_args):
        op = op_and_args[0]
        args = op_and_args[1:]
        return op.generator(*args)
        
    return [apply(op_and_args) for op_and_args in ops_and_args]