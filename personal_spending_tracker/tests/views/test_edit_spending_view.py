# Tests for edit spending view
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, ModelConcreteCategory, User, Spending, ConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *
from datetime import date, timedelta

class EditSpendingViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
        self.newSpending = Spending.objects.create(
            title = 'Test Transaction',
            description = 'Test',
            date = date.today(),
            amount = 5.00,
            is_regular = False,
            frequency = 'Monthly',
            next_due_date = date.today() + timedelta(days=30),
            user = self.user,
            category = self.newCategory
        )
        self.form_input = {
            'title': self.newSpending.title,
            'description': self.newSpending.description,
            'amount' : self.newSpending.amount,
            'is_regular' : self.newSpending.is_regular,
            'frequency' : self.newSpending.frequency,
            'next_due_date' : self.newSpending.next_due_date,
            'category': self.newSpending.category,
            'date' : self.newSpending.date
        }
        self.url = reverse('edit_spending', kwargs={'spending_id':self.newSpending.id})
        self.client.login(username=self.user.username, password='Password123')

    def test_edit_spending_url(self):
        self.assertEqual(self.url, f'/edit_spending/{self.newSpending.id}/')

    def test_get_edit_spending(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_edit_title(self):
        self.form_input['title'] = "New Title"
        response = self.client.post(self.url, self.form_input, follow=True)
        newTitle = Spending.objects.get(id=self.newSpending.id).title
        self.assertContains(response, newTitle)
        self.assertTrue(newTitle, self.form_input['title'])

    def test_edit_description(self):
        self.form_input['description'] = "New Description"
        response = self.client.post(self.url, self.form_input, follow=True)
        newDesc = Spending.objects.get(id=self.newSpending.id).description
        self.assertContains(response, newDesc)
        self.assertTrue(newDesc, self.form_input['description'])

    def test_edit_amount(self):
        self.form_input['amount'] = 10.69
        response = self.client.post(self.url, self.form_input, follow=True)
        newAmount = Spending.objects.get(id=self.newSpending.id).amount
        self.assertContains(response, newAmount)
        self.assertTrue(newAmount, self.form_input['amount'])

    def test_edit_date(self):
        self.form_input['date'] = date.today() - timedelta(days=1)
        response = self.client.post(self.url, self.form_input, follow=True)
        newDate = Spending.objects.get(id=self.newSpending.id).date
        self.assertContains(response, newDate)
        self.assertTrue(newDate, self.form_input['date'])

    def test_edit_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category 2',
            limit = 100,
            user = self.user
        )
        self.form_input['category'] = newCategory
        response = self.client.post(self.url, self.form_input, follow=True)
        newCategory = Spending.objects.get(id=self.newSpending.id).category.name
        self.assertContains(response, newCategory)
        self.assertTrue(newCategory, self.form_input['category'])

    def test_edit_is_regular(self):
        self.form_input['is_regular'] = True
        response = self.client.post(self.url, self.form_input, follow=True)
        newIsRegular = Spending.objects.get(id=self.newSpending.id).is_regular
        self.assertContains(response, newIsRegular)
        self.assertTrue(newIsRegular, self.form_input['is_regular'])
        

