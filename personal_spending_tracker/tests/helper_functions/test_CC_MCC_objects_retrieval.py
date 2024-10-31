from django.test import TestCase
from personal_spending_tracker.models import *
from personal_spending_tracker.helper_functions.cycle_objects_retrieval_and_modification import *
from  personal_spending_tracker.helper_functions import CC_MCC_objects_retrieval


class TestCycleObjectsRetrievalAndModification(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'ricksanchez',
            email = 'ricksanchez@example.com',
            password = 'Password123',
            first_name = 'Rick',
            last_name = 'Sanchez',
            bio = "Test",
            date_of_birth = '1958-07-03',
            cycle_length = 'MONTHLY'
        )
        self.cycle = Cycle.objects.create(
            user = self.user,
            start_date = date.today() - timedelta(days=7),
            cycle_length = 'WEEKLY'
        )
        self.newModelCategory = ModelConcreteCategory.objects.create(
            user = self.user,
            current_name = 'Test Category'
        )
        self.Category = ConcreteCategory.objects.create(
            name = self.newModelCategory.current_name,
            limit = 50,
            user = self.user,
            cycle = self.cycle,
            model_concrete_category = self.newModelCategory,
            goal_as_little_as_possible = 0,
            goal_well_distributed = 0,
            goal_x_less = 0
        )

    def test_get_model_concrete_categories(self):
        result = CC_MCC_objects_retrieval.get_model_concrete_categories(self.user)
        self.assertQuerysetEqual(result, [])

    def test_get_active_concrete_categories(self):
        result = CC_MCC_objects_retrieval.get_active_concrete_categories(self.category)
        self.assertIsNone(result)

    def test_get_active_model_concrete_categories(self):
        result = CC_MCC_objects_retrieval.get_active_model_concrete_categories(self.user)
        self.assertQuerysetEqual(result, [])

    def test_get_active_and_inactive_MCCs(self):
        active, inactive = CC_MCC_objects_retrieval.get_active_and_inactive_MCCs(self.user)
        self.assertQuerysetEqual(active, [])
        self.assertQuerysetEqual(inactive, [repr(self.category)])
