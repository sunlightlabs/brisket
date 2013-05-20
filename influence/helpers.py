from django.http import Http404
from django.template.defaultfilters import slugify
from settings import api, LATEST_CYCLE, DEFAULT_CYCLE
import datetime
import googleanalytics
import re
from django.utils.datastructures import SortedDict
from name_cleaver import PoliticianNameCleaver, OrganizationNameCleaver, \
        IndividualNameCleaver
from name_cleaver.names import PoliticianName


_standardizers = {
    'politician': lambda n: PoliticianNameCleaver(n).parse(),
    'individual': lambda n: IndividualNameCleaver(n).parse(),
    'industry': lambda n: OrganizationNameCleaver(n).parse(),
    'organization': lambda n: OrganizationNameCleaver(n).parse(),
}

def standardize_name(name, type):
    return _standardizers[type](name)

def bar_validate(data):
    ''' take a dict formatted for submission to the barchart
     generation function, and make sure there's data worth displaying.
     if so, return the original data. if not, return false.'''

    positive_data = [d for d in data if int(float(d['value'])) > 0]
    data = positive_data
    # if all the data is 0 or if the list with only positive data is
    # empty, return false
    if sum([int(float(record['value'])) for record in data]) == 0:
        return []
    else:
        return data

def pie_validate(data):
    ''' take a dict formatted for submission to the piechart
     generation function, and make sure there's data worth displaying.
     if so, return the original data. if not, return false.'''

    positive = {}
    for k,v in data.iteritems():
        if int(float(v)) != 0:
            positive[k] = v
    if len(positive) == 0:
        return []
    else:
        return positive

def barchart_href(record, cycle, entity_type):
    if record.get('recipient_entity', None):
            return str("/%s/%s/%s%s" % (entity_type, slugify(record['recipient_name']),
                                               record['recipient_entity'], "?cycle=" + cycle if cycle != "-1" else ""))
    elif record.get('id', None):
        if record['id']:
            return str("/%s/%s/%s%s" % (entity_type, slugify(record['name']),
                                               record['id'], "?cycle=" + cycle if cycle != "-1" else ""))
    return ''

def generate_label(string, max_length=34):
    ''' truncate names longer than max_length '''
    return string[:max_length] + (lambda x, l: (len(x)>l and "...")
                                   or "")(string, max_length)


section_indicators = {
   'individual':   {
       'contributions': ['contributor_count'],
       'lobbying': ['lobbying_count']},
   'organization': {
       'contributions': ['contributor_count', 'independent_expenditure_amount', 'fec_summary_count'],
       'lobbying': ['lobbying_count'],
       'fed_spending':['loan_count', 'grant_count', 'contract_count'],
       'earmarks': ['earmark_count'],
       'contractor_misconduct': ['contractor_misconduct_count'],
       'regulations': ['regs_document_count', 'regs_submitted_document_count'],
       'epa_echo': ['epa_actions_count'],
       'faca': ['faca_committee_count', 'faca_member_count']},
   'industry': {
       'contributions': ['contributor_count'],
       'lobbying': ['lobbying_count'],
       'fed_spending':['loan_count', 'grant_count', 'contract_count']},
   'politician':   {
       'contributions': ['recipient_count'],
       'earmarks': ['earmark_count']}
}

def get_data_types(entity_type, totals):
    data = {}
    for data_type, indicators in section_indicators[entity_type].iteritems():
        if (totals and
            [True for ind in indicators if totals[ind]]):
            data[data_type] = True
        else:
            data[data_type] = False
    return data

landing_page_section_indicators = {
    # GROUPS
   'industry': {
       'contributions': ['party_summary','pol_group_summary','state_fed_summary'], #,'office_type_summary'
       'lobbying': ['issues_summary','bills_summary'],
       #'fed_spending':['loan_summary', 'grant_summary', 'contract_summary']
       },
   'org': {
       'contributions': ['party_summary','pol_group_summary','state_fed_summary'], #,'office_type_summary'
       'lobbying': ['issues_summary','bills_summary'],
       #'fed_spending':['loan_summary', 'grant_summary', 'contract_summary'],
       #'earmarks': ['earmark_summary'],
       #'contractor_misconduct': ['contractor_misconduct_summary'],
       #'regulations': ['regs_document_summary', 'regs_submitted_document_summary'],
       #'epa_echo': ['epa_actions_summary'],
       #'faca': ['faca_committee_summary', 'faca_member_summary']
       },
   'pol_group': {
       'contributions': ['party_summary','pol_group_summary','state_fed_summary'], #,'office_type_summary'
       'lobbying': ['issues_summary','bills_summary'],
       #'regulations': ['regs_document_summary', 'regs_submitted_document_summary'],
       #'faca': ['faca_committee_summary', 'faca_member_summary']
       },
   'lobbying_firm': {
       'contributions': ['party_summary','pol_group_summary','state_fed_summary'], #,'office_type_summary'
       'lobbying': ['issues_summary','bills_summary'],
       #'regulations': ['regs_document_summary', 'regs_submitted_document_summary'],
       #'faca': ['faca_committee_summary', 'faca_member_summary']
       },
   # PEOPLE
   'contributor':   {
       'contributions': ['party_summary','pol_group_summary','state_fed_summary'], #,'office_type_summary'
       'lobbying': ['issues_summary','bills_summary']
       },
   'lobbyist':   {
       'contributions': ['party_summary','pol_group_summary','state_fed_summary'], #,'office_type_summary'
       'lobbying': ['issues_summary','bills_summary']},
   'pol':   {
       'contributions': ['recipient_summary'],
       'earmarks': ['earmark_summary']},
}

def get_metadata(entity_id, request, entity_type):
    entity_info = api.entities.metadata(entity_id)

    data = {}
    data['available_cycles'] = [c for c in entity_info['totals'].keys() if int(c) <= LATEST_CYCLE]

    if entity_info['years']:
        entity_info['years']['end'] = min(LATEST_CYCLE, entity_info['years']['end'])

    if 'cycle' in request.GET:
        cycle = str(request.GET['cycle'])
    else:
        cycle = str(DEFAULT_CYCLE)

    # check which types of data are available about this entity
    totals_for_cycle = entity_info['totals'].get(cycle, False)
    data.update(get_data_types(entity_type, totals_for_cycle))

    # discard the info from cycles that are not the current one
    if entity_info['totals'].get(cycle, None):
        entity_info['totals'] = entity_info['totals'][cycle]
    data['entity_info'] = entity_info

    return data, cycle

def get_summaries(entity_type, request):
    data = {}

    if 'cycle' in request.GET:
        cycle = str(request.GET['cycle'])
    else:
        cycle = str(DEFAULT_CYCLE)

    if 'limit' in request.GET:
        limit = str(request.GET['limit'])
    else:
        limit = str(-1)

    for data_type,indicators in landing_page_section_indicators[entity_type].iteritems():
        print 'summary for %s'%(data_type,)
        inds = {}
        for indicator in indicators:
            print  '>>> %s'%(indicator,)
            inds[indicator] = api.summaries.summarize(entity_type,indicator.replace('_summary',''),cycle=cycle,limit=limit)
        data[data_type] = inds

    return data,cycle
    #for data_type, indicators in section_indicators[entity_type].iteritems():
    #data['available_cycles'] = [c for c in en

def earmarks_table_data(entity_id, cycle):
    rows = api.pol.earmarks(entity_id, cycle)
    for row in rows:
        for member in row['members']:
            member_obj_or_str = PoliticianNameCleaver(member['name']).parse()
            if isinstance(member_obj_or_str, PoliticianName):
                member['name'] = str(member_obj_or_str.plus_metadata(member['party'], member['state']))
            else:
                member['name'] = member_obj_or_str

    return rows

def months_into_cycle_for_date(date, cycle):
    end_of_cycle = datetime.datetime.strptime("{0}1231".format(cycle), "%Y%m%d").date()
    step = 24 - abs(((end_of_cycle.year - date.year) * 12) + end_of_cycle.month - date.month)
    return step

def filter_bad_spending_descriptions(spending):
    for r in spending:
        if r['description'].count('!') > 10:
            r['description'] = ''


def get_source_display_name(metadata):
    source_display_names = {'wikipedia_info': 'Wikipedia', 'bioguide_info': 'Bioguide', 'sunlight_info': 'Sunlight'}
    return source_display_names.get(metadata.get('source_name', ''), '')

def make_bill_link(bill):
    if bill['bill_type'] in 'h hr hc hj s sr sc sj'.split():
        if bill['congress_no'] and int(bill['congress_no']) >= 109:
            return 'http://www.opencongress.org/bill/{0}-{1}{2}/show'.format(bill['congress_no'], bill['bill_type'], bill['bill_no'])

from influence.cache import cache

@cache(seconds=86400)
def get_top_pages():
    end_dt = datetime.datetime.now()

    end_date = end_dt.date()
    start_date = (end_dt - datetime.timedelta(days=7)).date()

    from django.conf import settings

    try:
        connection = googleanalytics.Connection(settings.GOOGLE_ANALYTICS_USER, settings.GOOGLE_ANALYTICS_PASSWORD)
        account = connection.get_account(settings.GOOGLE_ANALYTICS_PROFILE_ID)

        pages = account.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['pagePath','pageTitle'],
            metrics=['pageviews',],
            sort=['-pageviews']
        )
    except:
        return None

    entity_signature = re.compile(r'^/[\w\-]+/[\w\-]+/[a-f0-9-]{32,36}')
    entity_pages = [{
        'views': page.metric,
        'path': page.dimensions[0],
        'title': page.dimensions[1].split('|')[0].strip()
    } for page in pages if entity_signature.match(page.dimensions[0]) and 'error' not in page.dimensions[1].lower()]

    return entity_pages[:5]

# dummy class used in search
class DummyEntity(object):
    def __init__(self, metadata):
        self.metadata = metadata
