# Tests for accounts session 1 view
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import User, Cycle, ModelConcreteCategory, ConcreteCategory, Spending
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *

class AccountsSession1ViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

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
        self.url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':'All', 'categoryfilter':'All', 'cyclefilter':'Current'})
        self.client.login(username=self.user.username, password='Password123')

    def test_accounts_session_1_url(self):
        self.assertEqual(self.url, f'/accounts_session_1_add_additional_spendings_for_recent_cycle/All/All/Current')

    def test_get_accounts_session_1(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_session_1_add_additional_spendings_for_recent_cycle.html')

    def test_navbar_items(self):
        response = self.client.get(self.url)
        self.assert_navbar(response)

    def test_topbar_items(self):
        response = self.client.get(self.url)
        self.assert_topbar(response)
    
    def test_display_no_transactions_when_none(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//table/tr/td')
            self.assertEquals(filterDisplay.text, "No Transactions")

    def test_display_transactions_when_available(self):
        newSpending = Spending.objects.create(
            title = 'Test Transaction',
            amount = 5.00,
            user = self.user,
            category = self.newCategory
        )
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//table/tr/td')
            self.assertEquals(filterDisplay.text, newSpending.title)

    def test_display_correct_filter_all(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying All')

    def test_display_correct_filter_past_week(self):
        filter = 'Past Week'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_this_week(self):
        filter = 'This Week'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_past_month(self):
        filter = 'Past Month'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_this_month(self):
        filter = 'This Month'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_past_year(self):
        filter = 'Past Year'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_this_year(self):
        filter = 'This Year'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_category(self):
        filter = self.newCategory.name
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':filter, 'categoryfilter':'All', 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_past_week_with_category(self):
        categoryfilter = self.newCategory.name
        timefilter = 'Past Week'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter, 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_this_week_with_category(self):
        categoryfilter = self.newCategory.name
        timefilter = 'This Week'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter, 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_past_month_with_category(self):
        categoryfilter = self.newCategory.name
        timefilter = 'Past Month'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter, 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_this_month_with_category(self):
        categoryfilter = self.newCategory.name
        timefilter = 'This Month'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter, 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_past_year_with_category(self):
        categoryfilter = self.newCategory.name
        timefilter = 'Past Year'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter, 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_this_year_with_category(self):
        categoryfilter = self.newCategory.name
        timefilter = 'This Year'
        filter_url = reverse('accounts_session_1_add_additional_spendings_for_recent_cycle', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter, 'cyclefilter':'Current'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_add_transaction_button_redirects_to_add_spending_page(self):
        response = self.client.get(self.url)
        redirect_url = reverse('add_spending')
        with self.assertHTML(response) as html:
            addTransactionButton = html.findall('.//p/a')[1]
            self.assertHTML(addTransactionButton, f'a[href="{redirect_url}"]')

    def test_next_button_redirects_to_cycle_finance_report_page(self):
        response = self.client.get(self.url)
        redirect_url = reverse('cycle_finance_report')
        with self.assertHTML(response) as html:
            nextButton = html.find('.//center/a')
            self.assertHTML(nextButton, f'a[href="{redirect_url}"]')
            
    