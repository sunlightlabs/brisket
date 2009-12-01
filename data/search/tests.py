
from datetime import date

from django.test import TestCase

from dcdata.contribution.models import Contribution
from dcdata.models import Import
from search.queries import extract_query


class SimpleTest(TestCase):
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
        
        q = extract_query({'date': "<|1999-12-31"})
        self.assertEqual(2, Contribution.objects.filter(*q).count())
        
        
    def test_contributor(self):
        self.create_contribution(datestamp=date(2000,1,1), contributor_entity='1234')
        self.create_contribution(datestamp=date(2000,1,1), contributor_entity='1234')
        self.create_contribution(datestamp=date(2000,1,1), contributor_entity='5678')
        
        q = extract_query({'contributor': "in|1234"})
        self.assertEqual(2, Contribution.objects.filter(*q).count())