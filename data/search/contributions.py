"""
The schema used to search the Contribution model.

Defines the syntax of HTTP requests and how the requests are mapped into Django queries.
"""


from django.db.models.query_utils import Q

from dcdata.utils.sql import parse_date
from dcdata.contribution.models import Contribution
from schema import Operator, Schema, InclusionField, OperatorField


# Generator functions

def _seat_in_generator(*seats):
    return Q(seat__in=seats)

def _state_in_generator(*states):
    return Q(contributor_state__in=states)

def _date_before_generator(date):
    return Q(datestamp__lte=parse_date(date))

def _date_after_generator(date):
    return Q(datestamp__gte=parse_date(date))

def _date_between_generator(first, second):
    return Q(datestamp__range=(parse_date(first), parse_date(second)))

def _contributor_in_generator(*entities):    
    return Q(contributor_entity__in=entities) | Q(organization_entity__in=entities) | Q(parent_organization_entity__in=entities)
    
def _recipient_in_generator(*entities):
    return Q(recipient_entity__in=entities) | Q(committee_entity__in=entities)    

def _entity_in_generator(*entities):
    return _contributor_in_generator(*entities) | _recipient_in_generator(*entities)

def _amount_less_than_generator(amount):
    return Q(amount__lte=int(amount))

def _amount_greater_than_generator(amount):
    return Q(amount__gte=int(amount))

def _amount_between_generator(lower, upper):
    return Q(amount__range=(int(lower), int(upper)))

def _cycle_in_generator(*cycles):
    return Q(cycle__in=[int(cycle) for cycle in cycles])

def _jurisdiction_in_generator(*jurisdiction):
    return Q(transaction_namespace__in=jurisdiction)


# Strings used in the HTTP request syntax

LESS_THAN_OP = '<'
GREATER_THAN_OP = '>'
BETWEEN_OP = '><'

SEAT_FIELD = 'seat'
STATE_FIELD = 'state'
DATE_FIELD = 'date'
CONTRIBUTOR_FIELD ='contributor'
RECIPIENT_FIELD = 'recipient'
ENTITY_FIELD = 'entity'
AMOUNT_FIELD = 'amount'
CYCLE_FIELD = 'cycle'
JURISDICTION_FIELD = 'transaction_namespace'


# the final search schema

CONTRIBUTION_SCHEMA = Schema(
                             InclusionField(SEAT_FIELD, _seat_in_generator),
                             InclusionField(STATE_FIELD, _state_in_generator),
                             InclusionField(CYCLE_FIELD, _cycle_in_generator),
                             InclusionField(CONTRIBUTOR_FIELD, _contributor_in_generator),
                             InclusionField(RECIPIENT_FIELD, _recipient_in_generator),
                             InclusionField(ENTITY_FIELD, _entity_in_generator),
                             InclusionField(JURISDICTION_FIELD, _jurisdiction_in_generator),
                             OperatorField(DATE_FIELD,
                                   Operator(LESS_THAN_OP, _date_before_generator),
                                   Operator(GREATER_THAN_OP, _date_after_generator),
                                   Operator(BETWEEN_OP, _date_between_generator)),
                             OperatorField(AMOUNT_FIELD,
                                   Operator(LESS_THAN_OP, _amount_less_than_generator),
                                   Operator(GREATER_THAN_OP, _amount_greater_than_generator),
                                   Operator(BETWEEN_OP, _amount_between_generator)))


def filter_contributions(request):
    return Contribution.objects.filter(*CONTRIBUTION_SCHEMA.extract_query(request)).order_by()