from django.test import TestCase

from influence import names
from transparencydata import api

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
        return [ x['id'] for x in api.entity_search(name) if x['name'] == name ][0]

    def assertLength(self, length, results):
        self.assertEqual(length, len(results))


class ContributionsAPITests(APITest):

    def test_pol_contributors(self):
        self.assertLength(10, api.pol_contributors(self.PELOSI, CYCLE))

    def test_pol_local_breakdown(self):
        self.assertLength(2, api.pol_local_breakdown(self.PELOSI, CYCLE))

    def test_pol_contributor_type_breakdown(self):
        self.assertLength(2, api.pol_contributor_type_breakdown(self.PELOSI, CYCLE))

    def test_indiv_org_recipients(self):
        self.assertLength(8, api.indiv_org_recipients(self.PICKENS, CYCLE))

    def test_indiv_pol_recipients(self):
        self.assertLength(10, api.indiv_pol_recipients(self.PICKENS, CYCLE))

    def test_indiv_party_breakdown(self):
        self.assertLength(2, api.indiv_party_breakdown(self.PICKENS, CYCLE))

    def test_org_recipients(self):
        self.assertLength(10, api.org_recipients(self.BANKERS, CYCLE))

    def test_org_party_breakdown(self):
        self.assertLength(3, api.org_party_breakdown(self.BANKERS, CYCLE))

    def test_org_level_breakdown(self):
        self.assertLength(1, api.org_level_breakdown(self.BANKERS, CYCLE))

    def test_pol_sectors(self):
        self.assertLength(10, api.pol_sectors(self.PELOSI, CYCLE))


class EntityAPITests(APITest):

    def test_entity_search(self):
        self.assertLength(2, api.entity_search('pelosi'))

    def test_entity_metadata(self):
        bankers = api.entity_metadata(self.BANKERS)

        self.assertLength(10, bankers)
        self.assertFalse(bankers['metadata']['lobbying_firm'])

        nickles = api.entity_metadata(self.NICKLES)
        self.assertTrue(nickles['metadata']['lobbying_firm'])

    def test_entity_year_range(self):
        bankers = api.entity_metadata(self.BANKERS)
        self.assertEqual(dict(start='1990', end='2010'), bankers['years'])
        self.assertEqual(dict(start='1990', end='2010'), bankers['camp_fin_years'])
        self.assertEqual(dict(start='1998', end='2010'), bankers['lobbying_years'])
        self.assertEqual(dict(start='2006', end='2010'), bankers['spending_years'])

    def test_id_lookup(self):
        self.assertEqual([{"id": str(self.PELOSI)}], api.entity_id_lookup('urn:crp:recipient', self.PELOSI_CRP_ID))


class LobbyingAPITests(APITest):

    def test_org_registrants(self):
        self.assertLength(10, api.org_registrants(self.BANKERS, CYCLE))

    def test_org_issues(self):
        self.assertLength(10, api.org_issues(self.BANKERS, CYCLE))

    def test_org_lobbyists(self):
        self.assertLength(10, api.org_lobbyists(self.BANKERS, CYCLE))

    def test_indiv_registrants(self):
        self.assertLength(2, api.indiv_registrants(self.VAN_SCOYOC, CYCLE))

    def test_indiv_issues(self):
        self.assertLength(10, api.indiv_issues(self.VAN_SCOYOC, CYCLE))

    def test_indiv_clients(self):
        self.assertLength(10, api.indiv_clients(self.VAN_SCOYOC, CYCLE))

    def test_reg_clients(self):
        self.assertLength(10, api.org_registrant_clients(self.NICKLES, CYCLE))

    def test_reg_lobbyists(self):
        self.assertLength(9, api.org_registrant_lobbyists(self.NICKLES, CYCLE))

    def test_reg_issues(self):
        self.assertLength(10, api.org_registrant_issues(self.NICKLES, CYCLE))


class IndividualNameStandardizationTests(TestCase):

    def test_all_kinds_of_crazy(self):
        self.assertEqual('Stanford Z Rothschild', names.standardize_individual_name('ROTHSCHILD 212, STANFORD Z MR'))

    def test_jr_and_the_like_end_up_at_the_end(self):
        self.assertEqual('Frederick A "Tripp" Baird III', names.standardize_individual_name('Baird, Frederick A "Tripp" III'))

    def test_throw_out_mr(self):
        self.assertEqual('T Boone Pickens', names.standardize_individual_name('Mr T Boone Pickens'))
        self.assertEqual('T Boone Pickens', names.standardize_individual_name('Mr. T Boone Pickens'))
        self.assertEqual('T Boone Pickens', names.standardize_individual_name('Pickens, T Boone Mr'))
        self.assertEqual('John L Nau', names.standardize_individual_name(' MR JOHN L NAU,'))

    def test_keep_the_mrs(self):
        self.assertEqual('Mrs T Boone Pickens', names.standardize_individual_name('Mrs T Boone Pickens'))
        self.assertEqual('Mrs. T Boone Pickens', names.standardize_individual_name('Mrs. T Boone Pickens'))
        self.assertEqual('Mrs Stanford Z Rothschild', names.standardize_individual_name('ROTHSCHILD 212, STANFORD Z MRS'))

    def test_capitalize_roman_numeral_suffixes(self):
        self.assertEqual('Ken Cuccinelli II', names.standardize_individual_name('KEN CUCCINELLI II'))
        self.assertEqual('Ken Cuccinelli II', names.standardize_individual_name('CUCCINELLI II, KEN'))
        self.assertEqual('Ken Cuccinelli IV', names.standardize_individual_name('CUCCINELLI IV, KEN'))
        self.assertEqual('Ken Cuccinelli IX', names.standardize_individual_name('CUCCINELLI IX, KEN'))

    def test_capitalize_scottish_last_names(self):
        self.assertEqual('Ronald McDonald', names.standardize_individual_name('RONALD MCDONALD'))
        self.assertEqual('Old MacDonald', names.standardize_individual_name('OLD MACDONALD'))


class OrganizationNameStandardizationTests(TestCase):

    def test_capitalize_pac(self):
        self.assertEqual('Nancy Pelosi Leadership PAC', names.standardize_organization_name('NANCY PELOSI LEADERSHIP PAC'))

    def test_make_single_word_names_ending_in_pac_all_uppercase(self):
        self.assertEqual('ECEPAC', names.standardize_organization_name('ECEPAC'))

    def test_names_starting_with_PAC(self):
        self.assertEqual('PAC For Engineers', names.standardize_organization_name('PAC FOR ENGINEERS'))
        self.assertEqual('PAC 102', names.standardize_organization_name('PAC 102'))

    def test_doesnt_bother_names_containing_string_pac(self):
        self.assertEqual('Pacific Trust', names.standardize_organization_name('PACIFIC TRUST'))

    def test_capitalize_scottish_names(self):
        self.assertEqual('McDonnell Douglas', names.standardize_individual_name('MCDONNELL DOUGLAS'))
        self.assertEqual('MacDonnell Douglas', names.standardize_individual_name('MACDONNELL DOUGLAS'))

