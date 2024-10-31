# Tests for accounts session view
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import User, Spending, ConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class AccountsSessionViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'ricksanchez',
            email = 'ricksanchez@example.com',
            password = 'Password123',
            first_name = 'Rick',
            last_name = 'Sanchez',
            cycle_length = 'MONTHLY'
        )
        self.url = reverse('accounts_session')
        self.client.login(username=self.user.username, password='Password123')

    def test_accounts_session_url(self):
        self.assertEqual(self.url, '/accounts_session/')

    def test_get_accounts_session(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_session.html')

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)

    # Test for no categories
    def test_display_no_categories_when_none(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            categoryDisplay = html.find('.//table//tr/td')
            self.assertEquals(categoryDisplay, None)

    # Test for displaying categories
    def test_display_categories_when_present(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            categoryDisplay = html.find('.//table/tr/td')
            self.assertEquals(categoryDisplay.text, ' ' + newCategory.name + ' ')

    # Test edit cat
    def test_edit_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        form_input = {
        'name' : newCategory.name + 'Test',
        'limit' : newCategory.limit,
        'goal_as_little_as_possible' : newCategory.goal_as_little_as_possible,
        'goal_well_distributed' : newCategory.goal_well_distributed,
        'goal_x_less' : newCategory.goal_x_less
        }
        response = self.client.post(self.url, form_input)
        newName = ConcreteCategory.objects.get(id=newCategory.id).name
        self.assertContains(response, newName)

    # Test edit lim
    def test_edit_limit(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        form_input = {
        'name' : newCategory.name,
        'limit' : newCategory.limit + 5,
        'goal_as_little_as_possible' : newCategory.goal_as_little_as_possible,
        'goal_well_distributed' : newCategory.goal_well_distributed,
        'goal_x_less' : newCategory.goal_x_less
        }
        response = self.client.post(self.url, form_input)
        newLimit = ConcreteCategory.objects.get(id=newCategory.id).limit
        self.assertContains(response, newLimit)

    # Test minimal spending goal
    # def test_edit_goal_minimal_spending(self):
    #     newCategory = ConcreteCategory.objects.create(
    #         name = 'Test Category',
    #         limit = 50,
    #         user = self.user
    #     )
    #     # goal = False
    #     # print(goal)
    #     # print(newCategory.goal_as_little_as_possible)
    #     # if newCategory.goal_as_little_as_possible == False:
    #     #     goal = True
    #     # print(goal)
    #     form_input = {
    #     'name' : newCategory.name,
    #     'limit' : newCategory.limit,
    #     'goal_as_little_as_possible' : True,
    #     'goal_well_distributed' : newCategory.goal_well_distributed,
    #     'goal_x_less' : newCategory.goal_x_less
    #     }
    #     response = self.client.post(self.url, form_input, follow=True)
    #     new_goal_as_little_as_possible = ConcreteCategory.objects.get(id=newCategory.id).goal_as_little_as_possible
    #     print(new_goal_as_little_as_possible)
    #     self.assertNotEqual(newCategory.goal_as_little_as_possible, new_goal_as_little_as_possible)

    # Test delete
    # Test goals
    # Test confirm
    # Test correct information display
    