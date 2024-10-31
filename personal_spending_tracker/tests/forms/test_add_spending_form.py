import random
from django.test import TestCase
from datetime import datetime, timedelta, date
from personal_spending_tracker.forms import SpendingForm
from django.contrib.auth import get_user_model
from personal_spending_tracker.helper_functions.CC_MCC_objects_retrieval import get_active_concrete_categories
from personal_spending_tracker.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from personal_spending_tracker.helper_functions.cycle_dates_computation import *
from personal_spending_tracker.helper_functions.cycle_objects_retrieval_and_modification import *

FREQUENCY_CHOICES = [('monthly', 'Monthly'), ('yearly', 'Yearly')]

class SpendingFormTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        # Create a user with the username 'johndoe'

        self.user = UserModel.objects.create(
            username='johndoe',
            email='johndoe@example.com',
            first_name='John',
            last_name='Doe',
            bio='Hi im new.',
            cycle_length=random.choice([option[0] for option in CYCLE_LENGTH_OPTIONS]),
            date_of_birth=date.today() - timedelta(days=random.randint(16*365, 50*365))
        )

        template_category=TemplateCategory.objects.create(name='Food & Drink', limit=1000.00)

        model_concrete_category=ModelConcreteCategory.objects.create(
            current_name=template_category.name + f'{1}',
            user = self.user,
        )

        cycle=Cycle.objects.create(user=self.user, cycle_length=self.user.cycle_length, start_date = date.today())
        category=ConcreteCategory.objects.create(user=model_concrete_category.user, name=model_concrete_category.current_name + f'{1}', limit=500, cycle=cycle, model_concrete_category=model_concrete_category)


        self.form_input = {
            'title' : 'ExampleSpending',
            'description': 'Weekly groceries',
            'amount': 50.00,
            'photo': None,
            'category': category.model_concrete_category,
            'frequency': None,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'next_due_date': None,
            'is_regular': False,
            'user': self.user
            }

    def test_valid_form(self):
        data=self.form_input
        form = SpendingForm(user=self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_title(self):
        form_data = self.form_input.copy()
        form_data['title'] = ''
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_missing_description(self):
        form_data = self.form_input.copy()
        form_data['description'] = ''
        form = SpendingForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_missing_photo(self):
        form_data = self.form_input.copy()
        form_data['photo'] = None
        form = SpendingForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_missing_amount(self):
        form_data = self.form_input.copy()
        form_data['amount'] = None
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_invalid_form_missing_date(self):
        form_data = self.form_input.copy()
        form_data['date'] = None
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
    
    # def test_invalid_form_missing_category(self):
    #     form_data = {
    #         'title' : 'ExampleSpending',
    #         'description': 'Weekly groceries',
    #         'amount': 50.00,
    #         'photo': None,
    #         'category': '',
    #         'frequency': None,
    #         'date': datetime.now().strftime('%Y-%m-%d'),
    #         'next_due_date': None,
    #         'is_regular': False,
    #         'user': self.user
    #         }
        
    #     form = SpendingForm(user=self.user, data=form_data)
    #     self.assertFalse(form.is_valid())
    #     self.assertIn('category', form.errors)
    
    def test_invalid_form_date_outside_cycle_range(self):
        form_data = self.form_input.copy()
        # Define the range of dates to exclude
        cycle = get_the_active_cycle_for_user(self.user)
        start_date = cycle.start_date
        end_date = get_last_cycle_date(cycle)

        datetime_upper_limit = datetime.combine(start_date, datetime.min.time())
        random_timestamp = random.randint(0, (datetime_upper_limit - timedelta(days=1)).timestamp())
        random_date = datetime.fromtimestamp(random_timestamp).date()

        
        form_data['date'] = random_date
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_date_inside_cycle_range(self):
        form_data = self.form_input.copy()
        # Define the range of dates to exclude
        cycle = get_the_active_cycle_for_user(self.user)
        start_date = cycle.start_date
        end_date = get_last_cycle_date(cycle)

        delta = end_date - start_date
        random_date = start_date + timedelta(days=random.randint(0, delta.days))

        form_data['date'] = random_date
        form = SpendingForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_next_due_date_less_than_spending_date(self):
        form_data = self.form_input.copy()
        # Define the range of dates to exclude
        start_date = form_data['date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()

        datetime_upper_limit = datetime.combine(start_date_obj, datetime.min.time())
        random_timestamp = random.randint(0, (datetime_upper_limit - timedelta(days=1)).timestamp())
        random_date = datetime.fromtimestamp(random_timestamp).date()


        form_data['is_regular'] = True
        form_data['next_due_date'] = random_date
        form_data['frequency'] = random.choice([choice[0] for choice in FREQUENCY_CHOICES])
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_next_due_date_greater_than_spending_date(self):
        form_data = self.form_input.copy()
        # Define the range of dates to exclude
        start_date = form_data['date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()

        random_days = random.randint(1, 365)  # generate a random number of days
        random_date = start_date_obj + timedelta(days=random_days)  # add the random number of days to the start date


        form_data['is_regular'] = True
        form_data['next_due_date'] = random_date
        form_data['frequency'] = random.choice([choice[0] for choice in FREQUENCY_CHOICES])
        form = SpendingForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_next_due_date_not_filled_when_is_regular_checked(self):
        form_data = self.form_input.copy()


        form_data['is_regular'] = True
        form_data['frequency'] = random.choice([choice[0] for choice in FREQUENCY_CHOICES])
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_frequency_not_filled_when_is_regular_checked(self):
        form_data = self.form_input.copy()

        # Define the range of dates to exclude
        start_date = form_data['date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()

        random_days = random.randint(1, 365)  # generate a random number of days
        random_date = start_date_obj + timedelta(days=random_days)  # add the random number of days to the start date


        form_data['is_regular'] = True
        form_data['next_due_date'] = random_date
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_next_due_date_and_frequency_not_filled_when_is_regular_checked(self):
        form_data = self.form_input.copy()


        form_data['is_regular'] = True
        form = SpendingForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_save_correctly(self):
        form = SpendingForm(data=self.form_input, user=self.user)
        beforeCount = Spending.objects.count()
        form.save()
        afterCount = Spending.objects.count()
        self.assertEqual(afterCount, beforeCount+1)
        spending = Spending.objects.get(title='ExampleSpending')
        self.assertEqual(spending.title, self.form_input['title'])
        self.assertEqual(spending.description, self.form_input['description'])
        self.assertEqual(spending.amount, self.form_input['amount'])
        self.assertEqual(spending.category.model_concrete_category, self.form_input['category'])
        self.assertEqual(spending.frequency, self.form_input['frequency'])
        self.assertEqual(spending.date, datetime.strptime(self.form_input['date'], '%Y-%m-%d').date())
        self.assertEqual(spending.next_due_date, self.form_input['next_due_date'])
        self.assertEqual(spending.is_regular, self.form_input['is_regular'])
        self.assertEqual(spending.user, self.user)

    