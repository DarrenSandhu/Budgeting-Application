# Tests for edit profile view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, User
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class EditProfileViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
            cycle_length = 'WEEKLY'
        )
        self.url = reverse('edit_profile')
        self.client.login(username=self.user.username, password='Password123')

    def test_edit_profile_url(self):
        self.assertEqual(self.url, '/edit_profile/')

    def test_get_edit_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_navbar_items(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_succesful_edit_profile(self):
        form_input = {
            'username' : self.user.username,
            'email' : self.user.email,
            'bio' : 'Hi',
            'date_of_birth' : '1958-07-03'
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(User.objects.get(username=self.user.username).bio, form_input['bio'])
        self.assertTrue(User.objects.get(username=self.user.username).date_of_birth, form_input['date_of_birth'])
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_unsuccesful_edit_profile(self):
        form_input = {
            'username' : self.user.username,
            'email' : self.user.email,
            'bio' : 'Hi',
            'date_of_birth' : date.today()
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertFalse(User.objects.get(username=self.user.username).bio, form_input['bio'])
        self.assertFalse(User.objects.get(username=self.user.username).date_of_birth, form_input['date_of_birth'])
        with self.assertHTML(response) as html:
            errorMessage = html.find('.//form/ul/li')
            self.assertEquals(errorMessage.text, 'You must be at least 16 years old.')
            