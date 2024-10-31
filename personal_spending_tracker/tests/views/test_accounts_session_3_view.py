# Tests for accounts session 3 view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import PointReward, User, Cycle, ModelConcreteCategory, ConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class AccountsSession3ViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
        self.newModelCategory = ModelConcreteCategory.objects.create(
            user = self.user,
            current_name = 'Test Category'
        )
        self.newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user,
            cycle = self.new_active_cycle,
            model_concrete_category = self.newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )
        self.url = reverse('accounts_session_3_points_summary')
        self.client.login(username=self.user.username, password='Password123')

    def test_accounts_session_3_url(self):
        self.assertEqual(self.url, '/accounts_session_3_points_summary/')

    def test_get_accounts_session_3(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_session_3_points_summary.html')

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_display_no_points_achieved_when_none(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            pointsDisplay = html.find('.//table/tr/td')
            self.assertEquals(pointsDisplay.text, "No Points achieved")

    def test_display_points_when_available(self):
        newPoints = PointReward.objects.create(
            cycle = self.new_active_cycle,
            points = 10,
            rewarding_for = 'Test',
            category = self.newCategory
        )
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            pointsDisplay = html.find('.//table/tr/td')
            self.assertEquals(pointsDisplay.text, newPoints.rewarding_for)

    def test_next_button_redirects_to_accounts_session_page(self):
        response = self.client.get(self.url)
        redirect_url = reverse('accounts_session')
        with self.assertHTML(response) as html:
            nextButton = html.find('.//center/a')
            self.assertHTML(nextButton, f'a[href="{redirect_url}"]')
            