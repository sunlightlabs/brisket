
from datetime import date

from django.test import TestCase

from dcdata.contribution.models import Contribution
from dcdata.models import Import
from search.queries import extract_query


class SimpleTest(TestCase):
    def assert_num_results(self, expected_num, request):
        q = extract_query(request)
        self.assertEqual(expected_num, Contribution.objects.filter(*q).count())
    
    def create_contribution(self, **kwargs):
        c = Contribution(**kwargs)
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
        
        self.assert_num_results(1, {'date': "><|1999-12-24|1999-12-26"})
        self.assert_num_results(2, {'date': "<|1999-12-31"})
        self.assert_num_results(3, {'date': ">|1980-01-01"})

        
    def test_contributor(self):
        self.create_contribution(datestamp=date(2000,1,1), contributor_entity='1234')
        self.create_contribution(datestamp=date(2000,1,1), contributor_entity='1234')
        self.create_contribution(datestamp=date(2000,1,1), contributor_entity='5678')
        
        self.assert_num_results(2, {'contributor': "in|1234"})
        self.assert_num_results(3, {'contributor': "in|1234|5678"})
        
        