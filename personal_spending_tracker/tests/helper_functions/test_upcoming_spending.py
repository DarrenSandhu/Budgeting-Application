from django.test import TestCase
from datetime import date, timedelta
from calendar import monthrange
from personal_spending_tracker.models import User, Cycle, ConcreteCategory, Spending, ModelConcreteCategory
from  personal_spending_tracker.helper_functions import upcoming_spending


class RegularSpendingsTestCase(TestCase):
    def setUp(self):
        # create a test user and a test cycle
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cycle = Cycle.objects.create(user = self.user,
            start_date = date.today() - timedelta(days=7),
            cycle_length = 'WEEKLY')
        self.newModelCategory = ModelConcreteCategory.objects.create(
            user = self.user,
            current_name = 'Test Category'
        )
        self.category = ConcreteCategory.objects.create(
            name = self.newModelCategory.current_name,
            limit = 50,
            user = self.user,
            cycle = self.cycle,
            model_concrete_category = self.newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )

    def test_get_all_regular_spendings(self):
        # create a regular spending for the test user
        spending = Spending.objects.create(user=self.user)
        # test that the spending is returned by get_all_regular_spendings
        response = get_all_regular_spendings(self.user)
        self.assertIn(spending, response)

    def test_get_all_close_regular_spendings(self):
        # create a regular spending that is due in 2 days
        spending = Spending.objects.create(user=self.user)
        # test that the spending is returned by get_all_close_regular_spendings
        response = get_all_close_regular_spendings(self.user)
        self.assertIn(spending, response)

    def test_get_all_far_regular_spendings(self):
        # create a regular spending that is due in 4 days
        spending = Spending.objects.create(user=self.user)
        # test that the spending is returned by get_all_far_regular_spendings
        response = get_all_far_regular_spendings(self.user)
        self.assertIn(spending, response)
