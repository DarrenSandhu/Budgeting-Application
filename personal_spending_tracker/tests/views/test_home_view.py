# Tests for home view
from django.test import TestCase
from django.urls import reverse
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class HomeViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

    def setUp(self):
        self.url = reverse('home')

    def test_home_url(self):
        self.assertEqual(self.url, '/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # Test Sign Up Button
    def test_sign_up_button_redirects_to_sign_up_page(self):
        response = self.client.get(self.url)
        redirect_url = reverse('sign_up')
        with self.assertHTML(response) as html:
            signUpButton = html.find('.//p/a')
            self.assertHTML(signUpButton, f'a[href="{redirect_url}"]')

    # Test Log In Button
    def test_log_in_button_redirects_to_log_in_page(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        with self.assertHTML(response) as html:
            logInButton = html.findall('.//p/a')[1]
            self.assertHTML(logInButton, f'a[href="{redirect_url}"]')

    #Test absence of navbar and topbar items
    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_no_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_no_topbar(response)
        