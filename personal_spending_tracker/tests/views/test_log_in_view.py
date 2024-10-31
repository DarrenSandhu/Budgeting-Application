"""Log in view test"""
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.forms import LogInForm
from personal_spending_tracker.models import User
from personal_spending_tracker.tests.helpers import *
from with_asserts.mixin import AssertHTMLMixin

class LogInViewTestCase(TestCase, LogInTester, NavbarTester, TopbarTester, AssertHTMLMixin):

    def setUp(self):
        self.url = reverse('log_in')
        User.objects.create_user('johndoe',
        email = 'johndoe@example.com',
        password = 'Password123')

    #correct url ?
    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    #get request
    def test_get_log_in(self):
        resp = self.client.get(self.url)
        #render the page correctly
        self.assertEqual(resp.status_code, 200)
        #template that is rendered by the server
        self.assertTemplateUsed(resp, 'log_in.html')
        form = resp.context['form']
        #form is instance of SignUpForm
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    #Test absence of navbar and topbar items
    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_no_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_no_topbar(response)

    def test_unsuccesful_log_in(self):
        form_input = {'username' : 'johndoe', 'password': 'Wrong345'}
        resp = self.client.get(self.url, form_input)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'log_in.html')
        form = resp.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._user_is_logged_in())

    def test_succesful_log_in(self):
        form_input = {'username' : 'johndoe', 'password': 'Password123'}
        resp = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._user_is_logged_in())
        resp_url = reverse('feed')
        self.assertRedirects(resp, resp_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(resp, 'feed.html')

    # Test for error message (invalid credentials)
    def test_password_confirmation_error_message(self):
        form_input = {'username' : 'johndoe', 'password': '123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertFalse(self._user_is_logged_in())
        with self.assertHTML(response) as html:
            errorMessage = html.find('.//p/b')
            self.assertEquals(errorMessage.text, 'Invalid credentials')
            
