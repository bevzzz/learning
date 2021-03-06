# Built-in libraries
import re

# Third-party libraries
from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Local libraries
from functional_tests.base import FunctionalTest


TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling her the email has been sent
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search("http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Cannot find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Log out")
        )
        navbar = self.browser.find_element(By.CLASS_NAME, "navbar-text")
        self.assertIn(TEST_EMAIL, navbar.text)

        # Now she logs out
        self.browser.find_element(By.LINK_TEXT, "Log out").click()
        # She is logged out
        self.wait_for(
            lambda: self.browser.find_element(By.NAME, "email")
        )
        navbar = self.browser.find_element(By.CLASS_NAME, "navbar-text")
        self.assertNotIn(TEST_EMAIL, navbar.text)
