
from datetime import date
import gc

from django.test import TestCase

from dcdata.contribution.models import Contribution
from dcdata.models import Import
from search.contributions import filter_contributions
 

class SimpleTest(TestCase):
    def create_entities(self):
        self.create_contribution(contributor_entity='1234')
        self.create_contribution(organization_entity='1234')
        self.create_contribution(parent_organization_entity='5678')        
        self.create_contribution(recipient_entity='abcd')
        self.create_contribution(recipient_entity='efgh')
        self.create_contribution(committee_entity='efgh')  
        
    def assert_num_results(self, expected_num, request):
        self.assertEqual(expected_num, filter_contributions(request).count())
    
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
        
        self.assert_num_results(0, {'contributor': "abcd"})
        self.assert_num_results(1, {'contributor': "1234"})
        self.assert_num_results(1, {'contributor': "1234|5678"})
        
    def test_recipient(self):
        self.create_entities()

        self.assert_num_results(0, {'recipient': "1234"})
        self.assert_num_results(1, {'recipient': "abcd"})
        self.assert_num_results(2, {'recipient': "efgh"})
        self.assert_num_results(3, {'recipient': "abcd|efgh"})
        self.assert_num_results(3, {'recipient': "0000|abcd|efgh"})
        
    def test_entity(self):
        self.create_entities()    
        
        self.assert_num_results(0, {'entity': "0000"})
        self.assert_num_results(1, {'entity': "5678"})
        self.assert_num_results(2, {'entity': "5678|abcd"})
        
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
        
        self.assert_num_results(0, {'cycle': "08"})
        self.assert_num_results(1, {'cycle': "02"})
        self.assert_num_results(2, {'cycle': "04"})
        
    def test_state(self):
        self.create_contribution(contributor_state='CA')
        self.create_contribution(contributor_state='OR')
        self.create_contribution(contributor_state='OR')
        
        self.assert_num_results(0, {'state': "WA"})
        self.assert_num_results(1, {'state': "CA"})
        self.assert_num_results(2, {'state': "OR"})
        
    def test_conjunctions(self):
        self.create_contribution(contributor_state="WA", amount=1000, contributor_entity="1234")
        self.create_contribution(contributor_state="WA", amount=100, contributor_entity="1234")
        
        self.assert_num_results(0, {'state': "CA", 'amount': ">|500", 'entity': "1234"})
        self.assert_num_results(1, {'state': "WA", 'amount': ">|500", 'entity': "1234"})
        self.assert_num_results(1, {'amount': ">|500", 'entity': "1234"})
        
        
# not an actual test case because there are no Contribution records in the test database.
# instead, copy this code to a Django shell and run it there.

#class MemoryTests(TestCase):
#    def test_streaming(self):
#        self.assertEqual()
#        
#        i = 0;
#        for c in filter_contributions({'cycle': "2006"})[:1000000].iterator():
#            
#            i += 1
#            if i % 100000 == 0:
#                gc.collect()
#                raw_input("At %s records streamed...press any key to continue." % i)
        
