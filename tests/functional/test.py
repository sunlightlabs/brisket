from noseselenium.cases import SeleniumTestCaseMixin
from nose.tools import *
from nose.plugins.attrib import attr

import unittest

class TestSelenium(unittest.TestCase, SeleniumTestCaseMixin):

    def set_up(self):
        self.selenium.set_timeout(50000)

    @attr('selenium')
    def test_start(self):
        """ Tests the start page."""
        self.selenium.open("/")

    @attr('selenium')
    def test_people_list(self):
        self.selenium.open("/people")
        self.selenium.wait_for_page_to_load(30000)
        assert_equal("Individuals | Influence Explorer", self.selenium.get_title())
        assert_true(self.selenium.is_text_present("The following individuals have contributed the greatest dollar amounts during the current election cycle."))
        # Look for a sampling of people we expect to be there. This could of course change.
        assert_true(self.selenium.is_text_present("Fred Eychaner"))
        assert_true(self.selenium.is_text_present("Susan Groff"))

    @attr('selenium')
    def test_politician_list(self):
        self.selenium.open("/people")
        self.selenium.wait_for_page_to_load(30000)
        assert_equal("Individuals | Influence Explorer", self.selenium.get_title())
        assert_true(self.selenium.is_text_present("The following individuals have contributed the greatest dollar amounts during the current election cycle."))
        self.selenium.open("/politicians")
        self.selenium.wait_for_page_to_load(30000)
        assert_equal("Politicians | Influence Explorer", self.selenium.get_title())
        assert_true(self.selenium.is_text_present("The following politicians have received the greatest dollar amounts during the current election cycle."))
        # Look for a sampling of people we expect to be there. This could of course change.
        assert_true(self.selenium.is_text_present("Jerry Brown"))
        assert_true(self.selenium.is_text_present("Charles J Crist Jr"))
        assert_true(self.selenium.is_text_present("David Vitter"))

    @attr('selenium')
    def test_organization_list(self):
        self.selenium.open("/people")
        self.selenium.wait_for_page_to_load(30000)
        assert_equal("Individuals | Influence Explorer", self.selenium.get_title())
        assert_true(self.selenium.is_text_present("The following individuals have contributed the greatest dollar amounts during the current election cycle."))
        self.selenium.open("/organizations")
        self.selenium.wait_for_page_to_load(30000)
        assert_equal("Organizations | Influence Explorer", self.selenium.get_title())
        assert_true(self.selenium.is_text_present("The following organizations have contributed the greatest dollar amounts during the current election cycle."))
        # Look for a sampling of orgs we expect to be there. This could of course change.
        assert_true(self.selenium.is_text_present("ActBlue"))
        assert_true(self.selenium.is_text_present("Comcast"))
        assert_true(self.selenium.is_text_present("National Assn of Realtors"))

    @attr('selenium')
    def test_politician__jerry_brown__2010(self):
        self.do_entity_page("/politician/jerry-brown/9e2fefcd6d094276a82eef1845059e7e?cycle=2010", "Jerry Brown")

    @attr('selenium')
    def test_politician__jerry_brown__all(self):
        self.do_entity_page("/politician/jerry-brown/9e2fefcd6d094276a82eef1845059e7e?cycle=-1", "Jerry Brown")

    @attr('selenium')
    def test_indiv__jerry_perenchio__2010(self):
        self.do_entity_page("/individual/jerry-perenchio/d3b046c11b0247e7a0c29525a6c8647d?cycle=2010", "Jerry Perenchio")

    @attr('selenium')
    def test_indiv__jerry_perenchio__all(self):
        self.do_entity_page("/individual/jerry-perenchio/d3b046c11b0247e7a0c29525a6c8647d?cycle=-1", "Jerry Perenchio")

    @attr('selenium')
    def test_org__actblue__2010(self):
        self.do_entity_page("/organization/actblue/dca1ab34f315427aa001ffe34afec212?cycle=2010", "ActBlue")

    @attr('selenium')
    def test_org__actblue__all(self):
        self.do_entity_page("/organization/actblue/dca1ab34f315427aa001ffe34afec212?cycle=-1", "ActBlue")

    @attr('selenium')
    def test_industry__lawyers__2010(self):
        self.do_entity_page("/industry/lawyerslaw-firms/f50cf984a2e3477c8167d32e2b14e052?cycle=2010", "Lawyers/Law Firms")

    @attr('selenium')
    def test_industry__lawyers__all(self):
        self.do_entity_page("/industry/lawyerslaw-firms/f50cf984a2e3477c8167d32e2b14e052?cycle=-1", "Lawyers/Law Firms")


    def do_entity_page(self, url, name):
        self.selenium.open(url)
        self.selenium.wait_for_page_to_load(30000)
        assert_equal(name, self.selenium.get_text("xpath=/html/body/div[3]/div/div[3]/div/h2"))
        assert_false(self.selenium.is_visible('xpath=//*[@id="cycle_submit"]')) # this is the button that shows up if JS is broken

