# Tests for spending by category view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, ModelConcreteCategory, User, ConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class SpendingByCategoryViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'ricksanchez',
            email = 'ricksanchez@example.com',
            password = 'Password123',
            first_name = 'Rick',
            last_name = 'Sanchez',
            cycle_length = 'MONTHLY'
        )
        self.url = reverse('spending_by_category')
        self.client.login(username=self.user.username, password='Password123')

    def test_spending_by_category_url(self):
        self.assertEqual(self.url, '/spending_by_category/')

    def test_get_spending_by_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spending_by_category.html')

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_display_no_categories_when_none(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            categoryDisplay = html.findall('.//tr/td')
            self.assertEquals(categoryDisplay[0].text, 'No active categories')
            self.assertEquals(categoryDisplay[2].text, 'No inactive categories')

    def test_display_categories_when_available(self):
        new_active_cycle = Cycle.objects.create(
            user = self.user,
            start_date = date.today() - timedelta(days=7),
            cycle_length = self.user.cycle_length
        )
        newModelCategory = ModelConcreteCategory.objects.create(
            user = self.user,
            current_name = 'Test Category'
        )
        newCategory = ConcreteCategory.objects.create(
            name = newModelCategory.current_name,
            limit = 50,
            user = self.user,
            cycle = new_active_cycle,
            model_concrete_category = newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            categoryDisplay = html.find('.//tr/td')
            self.assertEquals(categoryDisplay.text, newCategory.name)

    def test_categories_redirect_to_spending_by_concrete_category(self):
        response = self.client.get(self.url)
        redirect_url = reverse('spending_by_category_concrete_category', kwargs={'timefilter':'All', 'categoryfilter':'All', 'cyclefilter':'Current'})
        with self.assertHTML(response) as html:
            categoryButton = html.find('.//p/a/button')
            self.assertHTML(categoryButton, f'a[href="{redirect_url}"]')