# Tests for edit and delete spending
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import Cycle, User, Spending, ConcreteCategory, ModelConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class EditAndDeleteSpendingTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
            user = self.user,
            title = 'Test Spending',
            description = 'Test',
            amount = 5.00,
            frequency = 'Monthly',
            date = date.today(),
            next_due_date = date.today() + timedelta(days=30),
            category = self.newCategory,
            is_regular = False
        )
        self.form_input = {
            'user' : self.user,
            'title' : self.newSpending.title,
            'description' : self.newSpending.description,
            'amount' : self.newSpending.amount,
            'frequency' : self.newSpending.frequency,
            'date' : self.newSpending.date,
            'next_due_date' : self.newSpending.next_due_date,
            'category': self.newSpending.category,
            'is_regular': self.newSpending.is_regular
        }
        self.url = reverse('edit_spending', kwargs={'spending_id':self.newSpending.id})
        self.client.login(username=self.user.username, password='Password123')

    def test_edit_title_successful(self):
        self.form_input['title'] = "New Title"
        response = self.client.post(self.url, self.form_input,follow=True)
        newTitle = Spending.objects.get(id=self.newSpending.id).title
        self.assertEqual(newTitle, self.form_input.get('title'))

    def test_edit_description_successful(self):
        self.form_input['description'] = "New Description"
        response = self.client.post(self.url, self.form_input,follow=True)
        newDesc = Spending.objects.get(id=self.newSpending.id).description
        self.assertEqual(newDesc, self.form_input.get('description'))

    def test_edit_amount_successful(self):
        self.form_input['amount'] = 10.00
        response = self.client.post(self.url, self.form_input,follow=True)
        newAmount = Spending.objects.get(id=self.newSpending.id).amount
        self.assertEqual(newAmount, self.form_input.get('amount'))

    def test_edit_category_successful(self):
        newModelCategory = ModelConcreteCategory.objects.create(
            user = self.user,
            current_name = 'New Category'
        )
        newCategory = ConcreteCategory.objects.create(
            name = 'New Category',
            limit = 50,
            user = self.user,
            cycle = self.new_active_cycle,
            model_concrete_category = newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )
        self.form_input['category'] = newCategory
        response = self.client.post(self.url, self.form_input,follow=True)
        newCat = Spending.objects.get(id=self.newSpending.id).category
        self.assertEqual(newCat, self.form_input.get('category'))

    def test_edit_date_successful(self):
        self.form_input['date'] = date.today() - timedelta(days=1)
        response = self.client.post(self.url, self.form_input,follow=True)
        newDate = Spending.objects.get(id=self.newSpending.id).date
        self.assertEqual(newDate, self.form_input.get('date'))

    def test_edit_is_regular_successful(self):
        self.form_input['is_regular'] = True
        response = self.client.post(self.url, self.form_input,follow=True)
        newIsRegular = Spending.objects.get(id=self.newSpending.id).is_regular
        self.assertEqual(newIsRegular, self.form_input.get('is_regular'))

    def test_edit_frequency_successful(self):
        self.form_input['is_regular'] = True
        self.form_input['frequency'] = 'Yearly'
        response = self.client.post(self.url, self.form_input,follow=True)
        newFrequency = Spending.objects.get(id=self.newSpending.id).frequency
        self.assertEqual(newFrequency, self.form_input.get('frequency'))

    def test_next_due_date_successful(self):
        self.form_input['is_regular'] = True
        self.form_input['frequency'] = 'Yearly'
        self.form_input['next_due_date'] = date.today() + timedelta(days=365)
        response = self.client.post(self.url, self.form_input,follow=True)
        newDueDate = Spending.objects.get(id=self.newSpending.id).next_due_date
        self.assertEqual(newDueDate, self.form_input.get('next_due_date'))

    def test_delete_spending(self):
        delete_url = reverse('delete_spending', kwargs={'spending_id':self.newSpending.id})
        beforeCount = Spending.objects.filter(user=self.user).count()
        response = self.client.post(delete_url, self.form_input,follow=True)
        afterCount = Spending.objects.filter(user=self.user).count()
        self.assertEqual(afterCount, beforeCount-1)
        
        