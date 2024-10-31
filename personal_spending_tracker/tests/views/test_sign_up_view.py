"""Sign up view test"""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from personal_spending_tracker.forms import SignUpForm
from django.urls import reverse
from personal_spending_tracker.models import User
from personal_spending_tracker.tests.helpers import *
from with_asserts.mixin import AssertHTMLMixin

class SignUpViewTestCase(TestCase, LogInTester, NavbarTester, TopbarTester, AssertHTMLMixin):

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
        'username' : 'janedoe',
        'email' : 'janedoe@example.com',
        'first_name' : 'Jane',
        'last_name' : 'Doe',
        'newPassword' : 'Password123',
        'passwordConfirmation' : 'Password123'
        }

    #correct url ?
    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    #get request
    def test_get_sign_up(self):
        resp = self.client.get(self.url)
        #render the page correctly
        self.assertEqual(resp.status_code, 200)
        #template that is rendered by the server
        self.assertTemplateUsed(resp, 'sign_up.html')
        form = resp.context['form']
        #form is instance of SignUpForm
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    #Test absence of navbar and topbar items
    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_no_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_no_topbar(response)

    def test_succesful_sign_up(self):
        beforeCount = User.objects.count()
        response = self.client.post(self.url, self.form_input,follow=True)
        afterCount = User.objects.count()
        self.assertEqual(afterCount, beforeCount+1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        user = User.objects.get(username='janedoe')
        self.assertEqual(user.email, 'janedoe@example.com')
        isPasswordCorrect = check_password('Password123', user.password)
        self.assertTrue(isPasswordCorrect)
        self.assertTrue(self._user_is_logged_in())

    def test_unsuccesful_sign_up(self):
        self.form_input['username'] = ''
        beforeCount = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        afterCount = User.objects.count()
        self.assertEqual(afterCount, beforeCount)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._user_is_logged_in())

    # Test for error message (password confirmation)
    def test_password_confirmation_error_message(self):
        self.form_input['passwordConfirmation'] = '123'
        beforeCount = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        afterCount = User.objects.count()
        self.assertEqual(afterCount, beforeCount)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._user_is_logged_in())
        with self.assertHTML(response) as html:
            errorMessage = html.find('.//form/ul/li')
            self.assertEquals(errorMessage.text, 'password confirmation must match the password')
            