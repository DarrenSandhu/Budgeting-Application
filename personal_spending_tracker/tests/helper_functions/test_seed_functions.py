from django.test import TestCase
from django.utils import timezone
from personal_spending_tracker.models import *
from personal_spending_tracker.helper_functions.views_time_frames import *
from personal_spending_tracker.helper_functions.points_processing import *
from personal_spending_tracker.management.commands import seed_functions


class TestSeedFunctions(TestCase):

    def setUp(self):
        self.num_users = 5
        self.usernames = ['user{}'.format(i) for i in range(self.num_users)]

    def test_seed_users(self):
        seed_functions.seed_users(self.num_users)
        self.assertEqual(User.objects.all().count(), self.num_users)
        for username in self.usernames:
            user = User.objects.get(username=username)
            self.assertEqual(user.first_name, 'First{}'.format(user.id))
            self.assertEqual(user.last_name, 'Last{}'.format(user.id))
            self.assertTrue(user.check_password('Password123'))

    def test_seed_cycles(self):
        seed_functions.seed_users(self.num_users)
        seed_functions.seed_cycles()
        self.assertEqual(Cycle.objects.all().count(), self.num_users*25) # 5 users x 20 cycles

    def test_seed_template_categories(self):
        seed_functions.seed_template_categories()
        self.assertEqual(TemplateCategory.objects.all().count(), 5)

    def test_seed_model_concrete_categories(self):
        seed_functions.seed_users(self.num_users)
        seed_functions.seed_template_categories()
        seed_functions.seed_model_concrete_categories()
        self.assertEqual(ModelConcreteCategory.objects.all().count(), self.num_users*2) # default 2 categories per user

    def test_seed_concrete_categories(self):
        seed_functions.seed_users(self.num_users)
        seed_functions.seed_template_categories()
        seed_functions.seed_model_concrete_categories()
        seed_functions.seed_cycles()
        seed_functions.seed_concrete_categories()
        self.assertEqual(ConcreteCategory.objects.all().count(), self.num_users*2*25) # 2 categories x 25 cycles

    def test_seed_spendings_in_the_monthly_cycle(self):
        seed_functions.seed_users(self.num_users)
        seed_functions.seed_template_categories()
        seed_functions.seed_model_concrete_categories()
        seed_functions.seed_cycles()
        seed_functions.seed_concrete_categories()
        seed_functions.seed_spendings_in_the_monthly_cycle()
        self.assertGreater(Spending.objects.all().count(), 0)
        


    