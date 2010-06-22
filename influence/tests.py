

from django.test import TestCase

from influence import api, helpers


CYCLE = 2008


class APITest(TestCase):
    is_initialized = False

    def __init__(self, *args, **kwargs):
        super(APITest, self).__init__(*args, **kwargs)

        if not APITest.is_initialized:
            APITest.PELOSI_CRP_ID = 'N00007360'
            APITest.PELOSI = api.entity_search('Nancy Pelosi (D)')[0]['id']
            APITest.PICKENS = api.entity_search('T. Boone Pickens')[0]['id']
            APITest.BANKERS = api.entity_search('American Bankers Assn')[0]['id']
            APITest.VAN_SCOYOC = api.entity_search('Stewart Van Scoyoc')[0]['id']
            APITest.NICKLES = api.entity_search('Nickles Group')[0]['id']

            APITest.is_initialized = True

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
        self.assertLength(7, api.indiv_org_recipients(self.PICKENS, CYCLE))

    def test_indiv_pol_recipients(self):
        self.assertLength(10, api.indiv_pol_recipients(self.PICKENS, CYCLE))

    def test_indiv_party_breakdown(self):
        self.assertLength(1, api.indiv_party_breakdown(self.PICKENS, CYCLE))

    def test_org_recipients(self):
        self.assertLength(10, api.org_recipients(self.BANKERS, CYCLE))

    def test_org_party_breakdown(self):
        self.assertLength(3, api.org_party_breakdown(self.BANKERS, CYCLE))

    def test_org_level_breakdown(self):
        self.assertLength(1, api.org_level_breakdown(self.BANKERS, CYCLE))

    def test_pol_sectors(self):
        self.assertLength(10, api.pol_sectors(self.PELOSI, CYCLE))

    def test_org_industries_for_sector(self):
        self.assertLength(5, api.org_industries_for_sector(self.PELOSI, 'H', CYCLE))


class EntityAPITests(APITest):

    def test_entity_search(self):
        self.assertLength(2, api.entity_search('pelosi'))

    def test_entity_metadata(self):
        bankers = api.entity_metadata(self.BANKERS, CYCLE)
        self.assertLength(7, bankers)
        self.assertFalse(bankers['metadata']['lobbying_firm'])

        nickles = api.entity_metadata(self.NICKLES, CYCLE)
        self.assertTrue(nickles['metadata']['lobbying_firm'])


    def test_id_lookup(self):
        self.assertEqual([{"id": self.PELOSI}], api.entity_id_lookup('urn:crp:recipient', self.PELOSI_CRP_ID))


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


class NameStandardizationTests(TestCase):

    def test_strip_party_affiliation(self):
        self.assertEqual('Nancy Pelosi', helpers.strip_party('Nancy Pelosi (D)'))

    def test_convert_to_title_case_converts_non_mixed_case_names_only(self):
        self.assertEqual('Emory Macdonald', helpers.convert_case('EMORY MACDONALD'))
        self.assertEqual('Emory MacDonald', helpers.convert_case('Emory MacDonald'))

    def test_change_last_first_to_first_last(self):
        self.assertEqual('Nancy Pelosi', helpers.convert_name_to_first_last('Pelosi, Nancy'))

    def test_standardize_politician_name(self):
        self.assertEqual('Emory Macdonald', helpers.standardize_politician_name('MACDONALD, EMORY (R)'))
        self.assertEqual('Emory MacDonald', helpers.standardize_politician_name('MacDonald, Emory (R)'))
        self.assertEqual('Nancy Pelosi', helpers.standardize_politician_name('Nancy Pelosi (D)'))
        self.assertEqual('Albert Gore', helpers.standardize_politician_name('Gore, Albert'))

