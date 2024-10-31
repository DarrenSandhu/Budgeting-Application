# Tests for add spending view
from datetime import date, datetime, timedelta
from random import random
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import CYCLE_LENGTH_OPTIONS, Cycle, ModelConcreteCategory, TemplateCategory, User, Spending, ConcreteCategory
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class AddSpendingViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
            current_name = 'TestCategory'
        )
        self.newCategory = ConcreteCategory.objects.create(
            name = 'TestCategory',
            limit = 50,
            user = self.user,
            cycle = self.new_active_cycle,
            model_concrete_category = self.newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )
        self.form_input = {
            'user' : self.user,
            'title' : 'Test Spending',
            'description' : 'Test',
            'amount' : 5.00,
            'date' : date.today(),
            'next_due_date' : date.today() + timedelta(days=30),
            'category': self.newModelCategory,
            'is_regular': False
        }
        self.url = reverse('add_spending')
        self.client.login(username=self.user.username, password='Password123')

    def test_add_spending_url(self):
        self.assertEqual(self.url, '/add_spending/')

    def test_get_add_spending(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_spending.html')

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)

    def test_add_spending_successful(self):
        beforeCount = Spending.objects.filter(user=self.user).count()
        response = self.client.post(self.url, self.form_input, follow=True)
        afterCount = Spending.objects.filter(user=self.user).count()
        self.assertEqual(afterCount, beforeCount+1)

    def test_add_spending_unsuccessful(self):
        beforeCount = Spending.objects.filter(user=self.user).count()
        self.form_input['title'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        afterCount = Spending.objects.filter(user=self.user).count()
        self.assertEqual(afterCount, beforeCount)
