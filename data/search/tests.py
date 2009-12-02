
from datetime import date

from django.test import TestCase

from dcdata.contribution.models import Contribution
from dcdata.models import Import
from search.contributions import CONTRIBUTION_SCHEMA
 

class SimpleTest(TestCase):
    def create_entities(self):
        self.create_contribution(contributor_entity='1234')
        self.create_contribution(organization_entity='1234')
        self.create_contribution(parent_organization_entity='5678')        
        self.create_contribution(recipient_entity='abcd')
        self.create_contribution(recipient_entity='efgh')
        self.create_contribution(committee_entity='efgh')  
        
    def assert_num_results(self, expected_num, request):
        q = CONTRIBUTION_SCHEMA.extract_query(request)
        self.assertEqual(expected_num, Contribution.objects.filter(*q).count())
    
    def create_contribution(self, **kwargs):
        c = Contribution(**kwargs)
        if 'cycle' not in kwargs:
            c.cycle='09'
        c.transaction_namespace='urn:unittest:transaction'
        c.import_reference=self.import_
        c.save()
        
    def setUp(self):
        print "Deleting database..."
        Import.objects.all().delete()
        Contribution.objects.all().delete()
        
        self.import_ = Import()
        self.import_.save()
        
        
    def test_date(self):
        self.create_contribution(datestamp=date(1999,12,25))
        self.create_contribution(datestamp=date(1999,12,31))
        self.create_contribution(datestamp=date(2000,1,1))
        
        self.assert_num_results(0, {'date': ">|2001-01-01"})
        self.assert_num_results(1, {'date': "><|1999-12-24|1999-12-26"})
        self.assert_num_results(2, {'date': "<|1999-12-31"})
        self.assert_num_results(3, {'date': ">|1980-01-01"})

        
    def test_contributor(self):
        self.create_entities()
        
        self.assert_num_results(0, {'contributor': "in|abcd"})
        self.assert_num_results(2, {'contributor': "in|1234"})
        self.assert_num_results(3, {'contributor': "in|1234|5678"})
        
    def test_recipient(self):
        self.create_entities()

        self.assert_num_results(0, {'recipient': "in|1234"})
        self.assert_num_results(1, {'recipient': "in|abcd"})
        self.assert_num_results(2, {'recipient': "in|efgh"})
        self.assert_num_results(3, {'recipient': "in|abcd|efgh"})
        self.assert_num_results(3, {'recipient': "in|0000|abcd|efgh"})
        
    def test_entity(self):
        self.create_entities()    
        
        self.assert_num_results(0, {'entity': "in|0000"})
        self.assert_num_results(1, {'entity': "in|5678"})
        self.assert_num_results(2, {'entity': "in|5678|abcd"})
        
    def test_amount(self):
        self.create_contribution(amount=100)
        self.create_contribution(amount=500)
        self.create_contribution(amount=800)
        
        self.assert_num_results(0, {'amount': ">|1000"})
        self.assert_num_results(0, {'amount': "<|50"})
        self.assert_num_results(1, {'amount': ">|600"})
        self.assert_num_results(2, {'amount': "<|500"})
        self.assert_num_results(3, {'amount': "><|100|800"})
        
    def test_cycle(self):
        self.create_contribution(cycle=02)
        self.create_contribution(cycle=04)
        self.create_contribution(cycle=04)
        
        self.assert_num_results(0, {'cycle': "=|08"})
        self.assert_num_results(1, {'cycle': "=|02"})
        self.assert_num_results(2, {'cycle': "=|04"})
        
    def test_state(self):
        self.create_contribution(contributor_state='CA')
        self.create_contribution(contributor_state='OR')
        self.create_contribution(contributor_state='OR')
        
        self.assert_num_results(0, {'state': "=|WA"})
        self.assert_num_results(1, {'state': "=|CA"})
        self.assert_num_results(2, {'state': "=|OR"})
        
    def test_conjunctions(self):
        self.create_contribution(contributor_state="WA", amount=1000, contributor_entity="1234")
        self.create_contribution(contributor_state="WA", amount=100, contributor_entity="1234")
        
        self.assert_num_results(0, {'state': "=|CA", 'amount': ">|500", 'entity': "in|1234"})
        self.assert_num_results(1, {'state': "=|WA", 'amount': ">|500", 'entity': "in|1234"})
        self.assert_num_results(1, {'amount': ">|500", 'entity': "in|1234"})
