# Tests for change password view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, User
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *
from django.contrib.auth.hashers import check_password

class ChangePasswordViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'ricksanchez',
            email = 'ricksanchez@example.com',
            password = 'Password123',
            first_name = 'Rick',
            last_name = 'Sanchez',
            cycle_length = 'MONTHLY'
        )
        self.new_active_cycle = Cycle.objects.create(
            user = self.user,
            start_date = date.today() - timedelta(days=7),
            cycle_length = 'MONTHLY'
        )
        self.form_input = {
        'old_password' : 'Password123',
        'new_password1' : 'NewPassword1',
        'new_password2' : 'NewPassword1'
        }
        self.url = reverse('change_password')
        self.client.login(username=self.user.username, password='Password123')

    def test_change_password_url(self):
        self.assertEqual(self.url, '/change_password/')

    def test_get_change_password(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_change_password_successful(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        user = User.objects.get(username=self.user.username)
        self.assertTrue(user.check_password(self.form_input.get('new_password1')))

    def test_change_password_unsuccessful(self):
        self.form_input['new_password1'] = ''
        self.form_input['new_password2'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        user = User.objects.get(username=self.user.username)
        self.assertFalse(user.check_password(self.form_input.get('new_password1')))

    # Test for error message (wrong old password)
    def test_wrong_old_password_error_message(self):
        self.form_input['old_password'] = '123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertFalse(check_password(User.objects.get(username=self.user).password, self.form_input['new_password1']))
        with self.assertHTML(response) as html:
            errorMessage = html.find('.//form/ul/li')
            self.assertEquals(errorMessage.text, 'Invalid old password')

    # Test for error message (password confirmation)
    def test_wrong_password_confirmation_error_message(self):
        self.form_input['new_password1'] = 'NewPassword123'
        self.form_input['new_password2'] = 'NewPassword456'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertFalse(check_password(User.objects.get(username=self.user).password, self.form_input['new_password1']))
        with self.assertHTML(response) as html:
            errorMessage = html.find('.//form/ul/li')
            self.assertEquals(errorMessage.text, "The new password fields didn't match.")

    # Test for error message (password entirely numeric)
    # def test_entirely_numeric_password_error_message(self):
    #     self.form_input['new_password1'] = '8905671234'
    #     self.form_input['new_password2'] = '8905671234'
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     self.assertFalse(check_password(User.objects.get(username=self.user).password, self.form_input['new_password1']))
    #     with self.assertHTML(response) as html:
    #         errorMessage = html.find('.//form/ul/li')
    #         self.assertEquals(errorMessage.text, 'This password is entirely numeric.')

    # # Test for error message (password too common)
    # def test_password_too_common_error_message(self):
    #     self.form_input['new_password1'] = 'password'
    #     self.form_input['new_password2'] = 'password'
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     self.assertFalse(check_password(User.objects.get(username=self.user).password, self.form_input['new_password1']))
    #     with self.assertHTML(response) as html:
    #         errorMessage = html.find('.//form/ul/li')
    #         self.assertEquals(errorMessage.text, 'This password is too common.')

    # # Test for error message (password too short)
    # def test_password_too_short_error_message(self):
    #     self.form_input['new_password1'] = 'Pass1'
    #     self.form_input['new_password2'] = 'Pass1'
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     self.assertFalse(check_password(User.objects.get(username=self.user).password, self.form_input['new_password1']))
    #     with self.assertHTML(response) as html:
    #         errorMessage = html.find('.//form/ul/li')
    #         self.assertEquals(errorMessage.text, 'This password is too short. It must contain at least 8 characters.')
            

