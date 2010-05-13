

from django.test import TestCase

from influence import api


PELOSI = 'ff96aa62d48f48e5a1e284efe74a0ba8'
PELOSI_CRP_ID = 'N00007360'
PICKENS = '945bcd0635bc434eacb7abcdcd38abea'
BANKERS = 'c039e8a46406458fbd3d48fd174554fd'
VAN_SCOYOC = '51d4f9790a27496682df37f1636240c1'
NICKLES = 'b361f45dc45444928a247f920c1ba35c'
CYCLE = 2008


class APITest(TestCase):
    def assertLength(self, length, results):
        self.assertEqual(length, len(results))


class ContributionsAPITests(APITest):

    def test_pol_contributors(self):
        self.assertLength(10, api.pol_contributors(PELOSI, CYCLE))
        
    def test_pol_local_breakdown(self):
        self.assertLength(2, api.pol_local_breakdown(PELOSI, CYCLE))

    def test_pol_contributor_type_breakdown(self):
        self.assertLength(2, api.pol_contributor_type_breakdown(PELOSI, CYCLE))

    def test_indiv_org_recipients(self):
        self.assertLength(6, api.indiv_org_recipients(PICKENS, CYCLE))
        
    def test_indiv_pol_recipients(self):
        self.assertLength(10, api.indiv_pol_recipients(PICKENS, CYCLE))
        
    def test_indiv_party_breakdown(self):
        self.assertLength(1, api.indiv_party_breakdown(PICKENS, CYCLE))
        
    def test_org_recipients(self):
        self.assertLength(10, api.org_recipients(BANKERS, CYCLE))
        
    def test_org_party_breakdown(self):
        self.assertLength(3, api.org_party_breakdown(BANKERS, CYCLE))
        
    def test_org_level_breakdown(self):
        self.assertLength(1, api.org_level_breakdown(BANKERS, CYCLE))
        
    def test_pol_sectors(self):
        self.assertLength(10, api.pol_sectors(PELOSI, CYCLE))
        
    def test_org_industries_for_sector(self):
        self.assertLength(5, api.org_industries_for_sector(PELOSI, 'H', CYCLE))

        
class EntityAPITests(APITest):
    
    def test_entity_search(self):
        self.assertLength(2, api.entity_search('pelosi'))
        
    def test_entity_metadata(self):
        self.assertLength(5, api.entity_metadata(PELOSI, CYCLE))
        
    def test_id_lookup(self):
        self.assertEqual([{"id": "ff96aa62d48f48e5a1e284efe74a0ba8"}], api.entity_id_lookup('urn:crp:recipient', PELOSI_CRP_ID))


class LobbyingAPITests(APITest):
    
    def test_org_registrants(self):
        self.assertLength(10, api.org_registrants(BANKERS, CYCLE))

    def test_org_issues(self):
        self.assertLength(10, api.org_issues(BANKERS, CYCLE))
        
    def test_org_lobbyists(self):
        self.assertLength(10, api.org_lobbyists(BANKERS, CYCLE))
        
    def test_indiv_registrants(self):
        self.assertLength(2, api.indiv_registrants(VAN_SCOYOC, CYCLE))
        
    def test_indiv_issues(self):
        self.assertLength(10, api.indiv_issues(VAN_SCOYOC, CYCLE))
        
    def test_indiv_clients(self):
        self.assertLength(10, api.indiv_clients(VAN_SCOYOC, CYCLE))
        
    def test_reg_clients(self):
        self.assertLength(10, api.org_registrant_clients(NICKLES, CYCLE))
        
    def test_reg_lobbyists(self):
        self.assertLength(9, api.org_registrant_lobbyists(NICKLES, CYCLE))
        
    def test_reg_issues(self):
        self.assertLength(10, api.org_registrant_issues(NICKLES, CYCLE))

        