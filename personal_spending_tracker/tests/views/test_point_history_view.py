# Tests for point history view
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.models import User, ConcreteCategory, ModelConcreteCategory, PointReward, Cycle
from with_asserts.mixin import AssertHTMLMixin
from personal_spending_tracker.tests.helpers import *
from datetime import date, timedelta

class PointHistoryViewTestCase(TestCase, AssertHTMLMixin, NavbarTester, TopbarTester):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'ricksanchez',
            email = 'ricksanchez@example.com',
            password = 'Password123',
            first_name = 'Rick',
            last_name = 'Sanchez',
            cycle_length = 'MONTHLY'
        )
        self.url = reverse('point_history', kwargs={'timefilter':'All', 'categoryfilter':'All'})
        self.client.login(username=self.user.username, password='Password123')

    def test_point_history_url(self):
        self.assertEqual(self.url, f'/point_history/All/All/')

    def test_get_point_history(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'point_history.html')

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
        newCycle = Cycle.objects.create(
            user = self.user,
            cycle_length='MONTHLY',
            start_date=date.today(),
            accounts_session_date = date.today() + timedelta(days=30)
        )
        newModelCategory = ModelConcreteCategory.objects.create(
            current_name = 'Test Category',
            user = self.user,
        )
        newCategory = ConcreteCategory.objects.create(
            name = newModelCategory.current_name,
            model_concrete_category = newModelCategory,
            limit = 50,
            user = self.user,
            cycle = newCycle
        )
        newPoints = PointReward.objects.create(
            cycle = newCycle,
            points = 10,
            rewarding_for = 'Test',
            category = newCategory
        )
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            pointsDisplay = html.find('.//table/tr/td')
            self.assertEquals(pointsDisplay.text, newPoints.rewarding_for)

    def test_display_correct_filter_all(self):
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying All')

    def test_display_correct_filter_past_week(self):
        filter = 'Past Week'
        filter_url = reverse('point_history', kwargs={'timefilter':filter, 'categoryfilter':'All'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_this_week(self):
        filter = 'This Week'
        filter_url = reverse('point_history', kwargs={'timefilter':filter, 'categoryfilter':'All'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_past_month(self):
        filter = 'Past Month'
        filter_url = reverse('point_history', kwargs={'timefilter':filter, 'categoryfilter':'All'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_this_month(self):
        filter = 'This Month'
        filter_url = reverse('point_history', kwargs={'timefilter':filter, 'categoryfilter':'All'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_past_year(self):
        filter = 'Past Year'
        filter_url = reverse('point_history', kwargs={'timefilter':filter, 'categoryfilter':'All'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_this_year(self):
        filter = 'This Year'
        filter_url = reverse('point_history', kwargs={'timefilter':filter, 'categoryfilter':'All'})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        filter = newCategory.name
        filter_url = reverse('point_history', kwargs={'timefilter':'All', 'categoryfilter':filter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + filter)

    def test_display_correct_filter_past_week_with_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        categoryfilter = newCategory.name
        timefilter = 'Past Week'
        filter_url = reverse('point_history', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_this_week_with_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        categoryfilter = newCategory.name
        timefilter = 'This Week'
        filter_url = reverse('point_history', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_past_month_with_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        categoryfilter = newCategory.name
        timefilter = 'Past Month'
        filter_url = reverse('point_history', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_this_month_with_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        categoryfilter = newCategory.name
        timefilter = 'This Month'
        filter_url = reverse('point_history', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_past_year_with_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        categoryfilter = newCategory.name
        timefilter = 'Past Year'
        filter_url = reverse('point_history', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)

    def test_display_correct_filter_this_year_with_category(self):
        newCategory = ConcreteCategory.objects.create(
            name = 'Test Category',
            limit = 50,
            user = self.user
        )
        categoryfilter = newCategory.name
        timefilter = 'This Year'
        filter_url = reverse('point_history', kwargs={'timefilter':timefilter, 'categoryfilter':categoryfilter})
        response = self.client.get(filter_url)
        with self.assertHTML(response) as html:
            filterDisplay = html.find('.//p/a')
            self.assertEquals(filterDisplay.text, 'Displaying ' + timefilter + ' and ' + categoryfilter)
            