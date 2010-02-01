"""
The schema used to search the Contribution model.

Defines the syntax of HTTP requests and how the requests are mapped into Django queries.
"""


from django.db.models.query_utils import Q

from dcdata.utils.sql import parse_date
from dcdata.contribution.models import Contribution
from schema import Operator, Schema, InclusionField, OperatorField


# Generator functions

def _seat_in_generator(query, *seats):
    return query.filter(seat__in=seats)

def _state_in_generator(query, *states):
    return query.filter(contributor_state__in=states)

def _date_before_generator(query, date):
    return query.filter(datestamp__lte=parse_date(date))

def _date_after_generator(query, date):
    return query.filter(datestamp__gte=parse_date(date))

def _date_between_generator(query, first, second):
    return query.filter(datestamp__range=(parse_date(first), parse_date(second)))
    
def _committee_in_generator(query, *entities):    
    return query.filter(committee_entity__in=entities)
        
def _contributor_in_generator(query, *entities):    
    return query.filter(contributor_entity__in=entities)
    
def _recipient_in_generator(query, *entities):
    return query.filter(Q(recipient_entity__in=entities) | Q(committee_entity__in=entities))    

def _organization_in_generator(query, *entities):
    return query.filter(Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities))

def _entity_in_generator(query, *entities):
    return query.filter(Q(contributor_entity__in=entities) | Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities) | Q(recipient_entity__in=entities) | Q(committee_entity__in=entities))

def _amount_less_than_generator(query, amount):
    return query.filter(amount__lte=int(amount))

def _amount_greater_than_generator(query, amount):
    return query.filter(amount__gte=int(amount))

def _amount_between_generator(query, lower, upper):
    return query.filter(amount__range=(int(lower), int(upper)))

def _cycle_in_generator(query, *cycles):
    return query.filter(cycle__in=[int(cycle) for cycle in cycles])

def _jurisdiction_in_generator(query, *jurisdiction):
    return query.filter(transaction_namespace__in=jurisdiction)


def _contributor_ft_generator(query, *searches):
    return _ft_generator(query, 'contributor_name', *searches)

def _organization_ft_generator(query, *searches):
    terms = _ft_terms(*searches)
    clause = " or ".join([_ft_clause('organization_name'), _ft_clause('parent_organization_name'), _ft_clause('contributor_employer')])
    return query.extra(where=[clause], params=[terms, terms, terms])

def _committee_ft_generator(query, *searches):
    return _ft_generator(query, 'committee_name', *searches)

def _recipient_ft_generator(query, *searches):
    return _ft_generator(query, 'recipient_name', *searches)

def _ft_generator(query, column, *searches):
    return query.extra(where=[_ft_clause(column)], params=[_ft_terms(*searches)])

def _ft_terms(*searches):
    return ' & '.join((' '.join(searches)).split(' '))

def _ft_clause(column):
    return "to_tsvector('datacommons', %s) @@ to_tsquery('datacommons', %%s)" % column

# Strings used in the HTTP request syntax

LESS_THAN_OP = '<'
GREATER_THAN_OP = '>'
BETWEEN_OP = '><'

SEAT_FIELD = 'seat'
STATE_FIELD = 'state'
DATE_FIELD = 'date'
ORGANIZATION_FIELD ='organization'
COMMITTEE_FIELD ='committee'
CONTRIBUTOR_FIELD ='contributor'
RECIPIENT_FIELD = 'recipient'
ENTITY_FIELD = 'entity'
AMOUNT_FIELD = 'amount'
CYCLE_FIELD = 'cycle'
JURISDICTION_FIELD = 'transaction_namespace'

CONTRIBUTOR_FT_FIELD = 'contributor_ft'
ORGANIZATION_FT_FIELD = 'organization_ft'
COMMITTEE_FT_FIELD = 'committee_ft'
RECIPIENT_FT_FIELD = 'recipient_ft'


# the final search schema

CONTRIBUTION_SCHEMA = Schema(
                             InclusionField(SEAT_FIELD, _seat_in_generator),
                             InclusionField(STATE_FIELD, _state_in_generator),
                             InclusionField(CYCLE_FIELD, _cycle_in_generator),
                             InclusionField(COMMITTEE_FIELD, _committee_in_generator),
                             InclusionField(CONTRIBUTOR_FIELD, _contributor_in_generator),
                             InclusionField(RECIPIENT_FIELD, _recipient_in_generator),
                             InclusionField(ENTITY_FIELD, _entity_in_generator),
                             InclusionField(JURISDICTION_FIELD, _jurisdiction_in_generator),
                             InclusionField(ORGANIZATION_FIELD, _organization_in_generator),
                             InclusionField(CONTRIBUTOR_FT_FIELD, _contributor_ft_generator),
                             InclusionField(ORGANIZATION_FT_FIELD, _organization_ft_generator),
                             InclusionField(COMMITTEE_FT_FIELD, _committee_ft_generator),
                             InclusionField(RECIPIENT_FT_FIELD, _recipient_ft_generator),
                             OperatorField(DATE_FIELD,
                                   Operator(LESS_THAN_OP, _date_before_generator),
                                   Operator(GREATER_THAN_OP, _date_after_generator),
                                   Operator(BETWEEN_OP, _date_between_generator)),
                             OperatorField(AMOUNT_FIELD,
                                   Operator(LESS_THAN_OP, _amount_less_than_generator),
                                   Operator(GREATER_THAN_OP, _amount_greater_than_generator),
                                   Operator(BETWEEN_OP, _amount_between_generator)))


def filter_contributions(request):    
    return CONTRIBUTION_SCHEMA.build_filter(Contribution.objects, request).order_by()