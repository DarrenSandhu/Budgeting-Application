# Tests for category management dashboard view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, ModelConcreteCategory, User, ConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class CatManDashboardViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
        self.url = reverse('category_management_dashboard')
        self.client.login(username=self.user.username, password='Password123')

    def test_category_management_dashboard_url(self):
        self.assertEqual(self.url, '/manage_categories_dashboard/')

    def test_get_category_management_dashboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_management_dashboard.html')

    def test_navbar_items(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assert_topbar(response)

    # Test for no categories
    def test_display_no_categories_when_none(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            categoryDisplay = html.find('.//form/td')
            self.assertEquals(categoryDisplay, None)

    # Test for displaying categories
    def test_display_categories_when_present(self):
        newModelCategory = ModelConcreteCategory.objects.create(
            user = self.user,
            current_name = 'Test Category'
        )
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user,
            cycle = self.new_active_cycle,
            model_concrete_category = newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            categoryDisplay = html.find('.//form/td')
            self.assertEquals(categoryDisplay.text, ' ' + newCategory.name + ' ')

    # def test_rename(self):
    #     newModelCategory = ModelConcreteCategory.objects.create(
    #         user = self.user,
    #         current_name = 'Test Category'
    #     )
    #     newCategory = ConcreteCategory.objects.create(
    #         name = 'Test Category',
    #         limit = 50,
    #         user = self.user,
    #         cycle = self.new_active_cycle,
    #         model_concrete_category = newModelCategory,
    #         goal_as_little_as_possible = 0,
    #         goal_well_distributed = 0,
    #         goal_x_less = 0
    #     )
    #     form_input = {
    #     'category_name' : 'New Category Name',
    #     'category' : newModelCategory
    #     }
    #     response = self.client.post(self.url, form_input, follow=True)
    #     newName = ConcreteCategory.objects.get(id=newCategory.id).name
    #     self.assertContains(response, newName)
    #     self.assertEquals(form_input.get('category_name'), newName)
            