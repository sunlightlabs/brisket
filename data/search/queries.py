
from django.db.models.query_utils import Q



class Op(object):
    def __init__(self, generator):
        self.generator = generator


def date_before_generator(date):
    return Q(datestamp__lte=date)

def date_after_generator(date):
    return Q(datestamp__gte=date)

def date_between_generator(first, second):
    return Q(datestamp__rang=(first,second))

class DateSearch(object):
    param_name = 'date'
    
    
    before_op = Op(date_before_generator)
    after_op = Op(date_after_generator)
    between_op = Op(date_between_generator)
    
    
def contributor_in_generator(*entities):    
    return Q(contributor_entity__in=entities) | Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities)
    
class ContributorSearch(object):
    in_op = Op(contributor_in_generator)
    
def recipient_in_generator(entities):
    return Q(recipient_entity__in=entities) | Q(committee_entity__in=entities)    
    
class RecipientSearch(object):
    in_op = Op(recipient_in_generator)


def build_query(ops_and_args):
    def apply(op_and_args):
        op = op_and_args[0]
        args = op_and_args[1:]
        return op.generator(*args)
        
    return [apply(op_and_args) for op_and_args in ops_and_args]