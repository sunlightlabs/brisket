from django.test import TestCase
from settings import api

CYCLE = 2008


class APITest(TestCase):
    def setUp(self):
        APITest.PELOSI_CRP_ID = 'N00007360'
        APITest.PELOSI = self.find_exact_name_match('Nancy Pelosi (D)')
        APITest.PICKENS = self.find_exact_name_match('MR T BOONE PICKENS')
        APITest.BANKERS = self.find_exact_name_match('American Bankers Assn')
        APITest.VAN_SCOYOC = self.find_exact_name_match('Van Scoyoc, H Stewart')
        APITest.NICKLES = self.find_exact_name_match('Nickles Group')

    def find_exact_name_match(self, name):
        return [ x['id'] for x in api.entities.search(name) if x['name'] == name ][0]

    def assertLength(self, length, results):
        self.assertEqual(length, len(results))


class ContributionsAPITests(APITest):

    def test_pol_contributors(self):
        self.assertLength(10, api.pol.contributors(self.PELOSI, CYCLE))

    def test_pol_local_breakdown(self):
        self.assertLength(2, api.pol.local_breakdown(self.PELOSI, CYCLE))

    def test_pol_contributor_type_breakdown(self):
        self.assertLength(2, api.pol.contributor_type_breakdown(self.PELOSI, CYCLE))

    def test_indiv_org_recipients(self):
        self.assertLength(8, api.indiv.org_recipients(self.PICKENS, CYCLE))

    def test_indiv_pol_recipients(self):
        self.assertLength(10, api.indiv.pol_recipients(self.PICKENS, CYCLE))

    def test_indiv_party_breakdown(self):
        self.assertLength(2, api.indiv.party_breakdown(self.PICKENS, CYCLE))

    def test_org_recipients(self):
        self.assertLength(10, api.org.recipients(self.BANKERS, CYCLE))

    def test_org_party_breakdown(self):
        self.assertLength(3, api.org.party_breakdown(self.BANKERS, CYCLE))

    def test_org_level_breakdown(self):
        self.assertLength(1, api.org.level_breakdown(self.BANKERS, CYCLE))

    def test_pol_sectors(self):
        self.assertLength(10, api.pol.sectors(self.PELOSI, CYCLE))


class EntityAPITests(APITest):

    def test_entity_search(self):
        self.assertLength(2, api.entities.search('pelosi'))

    def test_entity_metadata(self):
        bankers = api.entities.metadata(self.BANKERS)

        self.assertLength(10, bankers)
        self.assertFalse(bankers['metadata']['lobbying_firm'])

        nickles = api.entities.metadata(self.NICKLES)
        self.assertTrue(nickles['metadata']['lobbying_firm'])

    def test_entity_year_range(self):
        bankers = api.entities.metadata(self.BANKERS)
        self.assertEqual(dict(start='1990', end='2010'), bankers['years'])
        self.assertEqual(dict(start='1990', end='2010'), bankers['camp_fin_years'])
        self.assertEqual(dict(start='1998', end='2010'), bankers['lobbying_years'])
        self.assertEqual(dict(start='2006', end='2010'), bankers['spending_years'])

    def test_id_lookup(self):
        self.assertEqual([{"id": str(self.PELOSI)}], api.entities.id_lookup('urn:crp:recipient', self.PELOSI_CRP_ID))


class LobbyingAPITests(APITest):

    def test_org_registrants(self):
        self.assertLength(10, api.org.registrants(self.BANKERS, CYCLE))

    def test_org_issues(self):
        self.assertLength(10, api.org.issues(self.BANKERS, CYCLE))

    def test_org_lobbyists(self):
        self.assertLength(10, api.org.lobbyists(self.BANKERS, CYCLE))

    def test_indiv_registrants(self):
        self.assertLength(2, api.indiv.registrants(self.VAN_SCOYOC, CYCLE))

    def test_indiv_issues(self):
        self.assertLength(10, api.indiv.issues(self.VAN_SCOYOC, CYCLE))

    def test_indiv_clients(self):
        self.assertLength(10, api.indiv.clients(self.VAN_SCOYOC, CYCLE))

    def test_reg_clients(self):
        self.assertLength(10, api.org.registrant_clients(self.NICKLES, CYCLE))

    def test_reg_lobbyists(self):
        self.assertLength(9, api.org.registrant_lobbyists(self.NICKLES, CYCLE))

    def test_reg_issues(self):
        self.assertLength(10, api.org.registrant_issues(self.NICKLES, CYCLE))


