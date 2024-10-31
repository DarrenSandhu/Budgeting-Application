# Tests for feed view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, User
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class FeedViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
        self.url = reverse('feed')
        self.client.login(username=self.user.username, password='Password123')

    def test_feed_url(self):
        self.assertEqual(self.url, '/feed/')

    def test_get_feed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_navbar_items(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_add_spending_button_redirects_to_add_spending_page(self):
        response = self.client.get(self.url)
        redirect_url = reverse('add_spending')
        with self.assertHTML(response) as html:
            addTransactionButton = html.find('.//a')
            self.assertHTML(addTransactionButton, f'a[href="{redirect_url}"]')
            
    