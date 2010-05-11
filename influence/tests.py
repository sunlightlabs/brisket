

from django.test import TestCase

from influence import api


PELOSI = 'ff96aa62d48f48e5a1e284efe74a0ba8'
PICKENS = '945bcd0635bc434eacb7abcdcd38abea'
BANKERS = 'c039e8a46406458fbd3d48fd174554fd'
VAN_SCOYOC = '51d4f9790a27496682df37f1636240c1'
CYCLE = 2008
LIMIT = 10


class ContributionsAPITests(TestCase):

    def test_pol_contributors(self):
        results = api.pol_contributors(PELOSI, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_pol_local_breakdown(self):
        results = api.pol_local_breakdown(PELOSI, CYCLE)
        self.assertEqual(2, len(results))

    def test_pol_contributor_type_breakdown(self):
        results = api.pol_contributor_type_breakdown(PELOSI, CYCLE)
        self.assertEqual(2, len(results))

    def test_indiv_org_recipients(self):
        results = api.indiv_org_recipients(PICKENS, CYCLE)
        self.assertEqual(6, len(results))
        
    def test_indiv_pol_recipients(self):
        results = api.indiv_pol_recipients(PICKENS, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_indiv_party_breakdown(self):
        results = api.indiv_party_breakdown(PICKENS, CYCLE)
        self.assertEqual(1, len(results))
        
    def test_org_recipients(self):
        results = api.org_recipients(BANKERS, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_org_party_breakdown(self):
        results = api.org_party_breakdown(BANKERS, CYCLE)
        self.assertEqual(3, len(results))
        
    def test_org_level_breakdown(self):
        results = api.org_level_breakdown(BANKERS, CYCLE)
        self.assertEqual(1, len(results))
        
    def test_pol_sectors(self):
        results = api.pol_sectors(PELOSI, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_org_industries_for_sector(self):
        results = api.org_industries_for_sector(PELOSI, 'H', CYCLE)
        self.assertEqual(5, len(results))
        
# todo: test ID lookup
class EntityAPITests(TestCase):
    
    def test_entity_search(self):
        results = api.entity_search('pelosi')
        self.assertEqual(2, len(results))
        
    def test_entity_metadata(self):
        results = api.entity_metadata(PELOSI, CYCLE)
        self.assertEqual(5, len(results))    


class LobbyingAPITests(TestCase):
    
    def test_org_registrants(self):
        results = api.org_registrants(BANKERS, CYCLE)
        self.assertEqual(10, len(results))

    def test_org_issues(self):
        results = api.org_issues(BANKERS, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_org_lobbyists(self):
        results = api.org_lobbyists(BANKERS, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_indiv_registrants(self):
        results = api.indiv_registrants(VAN_SCOYOC, CYCLE)
        self.assertEqual(2, len(results))
        
    def test_indiv_issues(self):
        results = api.indiv_issues(VAN_SCOYOC, CYCLE)
        self.assertEqual(10, len(results))
        
    def test_indiv_clients(self):
        results = api.indiv_clients(VAN_SCOYOC, CYCLE)
        self.assertEqual(10, len(results))
        

        