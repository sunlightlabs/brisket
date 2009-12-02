"""
The schema used to search the Contribution model.

Defines the syntax of HTTP requests and how the requests are mapped into Django queries.
"""

from datetime import date

from django.db.models.query_utils import Q

from schema import Operator, Field, Schema


# Generator functions

def _date_from_string(string_val):
    (year, month, day) = string_val.split('-')
    return date(int(year), int(month), int(day))

def _state_equals_generator(state):
    return Q(contributor_state=state)

def _date_before_generator(date):
    return Q(datestamp__lte=_date_from_string(date))

def _date_after_generator(date):
    return Q(datestamp__gte=_date_from_string(date))

def _date_between_generator(first, second):
    return Q(datestamp__range=(_date_from_string(first), _date_from_string(second)))

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

def _cycle_equals_generator(cycle):
    return Q(cycle=int(cycle))


# Strings used in the HTTP request syntax

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


# the final search schema

CONTRIBUTION_SCHEMA = Schema(Field(STATE_FIELD,
                                   Operator(EQUALS_OP, _state_equals_generator)),
                             Field(DATE_FIELD,
                                   Operator(LESS_THAN_OP, _date_before_generator),
                                   Operator(GREATER_THAN_OP, _date_after_generator),
                                   Operator(BETWEEN_OP, _date_between_generator)),
                             Field(CONTRIBUTOR_FIELD,
                                   Operator(IN_OP, _contributor_in_generator)),
                             Field(RECIPIENT_FIELD,
                                   Operator(IN_OP, _recipient_in_generator)),
                             Field(ENTITY_FIELD,
                                   Operator(IN_OP, _entity_in_generator)),
                             Field(AMOUNT_FIELD,
                                   Operator(LESS_THAN_OP, _amount_less_than_generator),
                                   Operator(GREATER_THAN_OP, _amount_greater_than_generator),
                                   Operator(BETWEEN_OP, _amount_between_generator)),
                             Field(CYCLE_FIELD,
                                   Operator(EQUALS_OP, _cycle_equals_generator)))


