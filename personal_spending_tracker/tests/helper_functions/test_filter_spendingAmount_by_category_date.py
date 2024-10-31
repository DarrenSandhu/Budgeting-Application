from django.test import TestCase
from personal_spending_tracker.models import User, ConcreteCategory, Cycle, Spending
from datetime import datetime, timedelta
from  personal_spending_tracker.helper_functions import filter_spendingAmount_by_category_date
class TestSpendingsFunctions(TestCase):
    
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # create a test category
        self.category = ConcreteCategory.objects.create(user=self.user, name='TestCategory', limit=1000)
        # create a test cycle
        self.cycle = Cycle.objects.create(user=self.user, start_date=datetime.today()-timedelta(days=30), cycle_length='MONTHLY')
        # create some test spendings
        self.spending1 = Spending.objects.create(user=self.user, category=self.category, title='TestSpending1', amount=50, date=datetime.today()-timedelta(days=1))
        self.spending2 = Spending.objects.create(user=self.user, category=self.category, title='TestSpending2', amount=100, date=datetime.today()-timedelta(days=7))
        self.spending3 = Spending.objects.create(user=self.user, category=self.category, title='TestSpending3', amount=200, date=datetime.today()-timedelta(days=31))
    
    def test_total_spendings_amount_in_chosen_category(self):
        # test total spending amount in a category
        total_spending = filter_spendingAmount_by_category_date.total_spendings_amount_in_chosen_category(self.user, self.category.id)
        self.assertEqual(total_spending, 350)
    
   