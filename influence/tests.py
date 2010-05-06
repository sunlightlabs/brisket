

from django.test import TestCase

from influence.api import AggregatesAPI


api = AggregatesAPI()
PELOSI = 'ff96aa62d48f48e5a1e284efe74a0ba8'
PICKENS = '945bcd0635bc434eacb7abcdcd38abea'
BANKERS = 'c039e8a46406458fbd3d48fd174554fd'
CYCLE = 2008
LIMIT = 10


# todo: inconsistent use of cycle and limit parameters.
# todo: remove all 'type' parameters
# todo: remove keyword args, or at least use them consistently
class ContributionsAPITests(TestCase):

    def test_pol_contributors(self):
        results = api.pol_contributors(PELOSI, 'unused field?', CYCLE)
        self.assertEqual(10, len(results))
        
    def test_pol_breakdown(self):
        results = api.pol_breakdown(PELOSI, 'local', CYCLE)
        self.assertEqual(2, len(results))

        results = api.pol_breakdown(PELOSI, 'entity', CYCLE)
        self.assertEqual(2, len(results))

    def test_indiv_org_recipients(self):
        results = api.indiv_org_recipients(PICKENS, CYCLE)
        self.assertEqual(6, len(results))
        
    def test_indiv_pol_recipients(self):
        results = api.indiv_pol_recipients(PICKENS, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_indiv_breakdown(self):
        results = api.indiv_breakdown(PICKENS, 'party', CYCLE)
        self.assertEqual(1, len(results))
        
    def test_org_recipients(self):
        results = api.org_recipients(BANKERS, cycle=CYCLE, limit=LIMIT)
        self.assertEqual(10, len(results))
        
    def test_org_breakdown(self):
        results = api.org_breakdown(BANKERS, 'party', CYCLE)
        self.assertEqual(2, len(results))
        
        results = api.org_breakdown(BANKERS, 'level', CYCLE)
        self.assertEqual(1, len(results))
        
    # todo: rename to have org/pol/indiv prefix
    def test_top_sectors(self):
        results = api.top_sectors(PELOSI, cycle=CYCLE, limit=LIMIT)
        self.assertEqual(10, len(results))
        
    # todo: rename
    # todo: seems completely broken
    def test_contributions_by_sector(self):
        results = api.contributions_by_sector(PELOSI, 'H')
        

class EntityAPITests(TestCase):
    
    def test_entity_search(self):
        results = api.entity_search('pelosi')
        self.assertEqual(2, len(results))
        
    def test_entity_metadata(self):
        results = api.entity_metadata(PELOSI, CYCLE)
        self.assertEqual(5, len(results))    

# rename to consistent scheme
class LobbyingAPITests(TestCase):
    
    def test_lobbying_for_org(self):
        results = api.lobbying_for_org(BANKERS, CYCLE)
        self.assertEqual(10, len(results))

    def test_issues_lobbied_for(self):
        results = api.issues_lobbied_for(BANKERS, CYCLE)
        self.assertEqual(10, len(results))
        
        
        