import os
from pathlib import Path
import shutil
from faker import Faker
import random
from random import randint, choice
from budgeting_app.settings import MEDIA_ROOT
from personal_spending_tracker.helper_functions.views_time_frames import *
from personal_spending_tracker.helper_functions.points_processing import *
from personal_spending_tracker.models import *
from datetime import date, timedelta
from django.utils import timezone
    
def seed_users(num_users=5):
    """Create `num_users` number of random users."""
    for i in range(num_users):
        username = f'user{i}'
        email = f'{username}@example.com'
        first_name = f'First{i}'
        last_name = f'Last{i}'
        cycle_length = random.choice([option[0] for option in CYCLE_LENGTH_OPTIONS])
        # Generate a random date of birth more than 16 years ago
        date_of_birth = date.today() - timedelta(days=random.randint(16*365, 50*365))
        bio = ' '.join(['Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit.', 'Fusce', 'non', 'neque', 'vel', 'ligula', 'porttitor', 'interdum', 'ac', 'et', 'quam.', 'Donec', 'sodales', 'quam', 'in', 'ante', 'dignissim', 'tempus.'])
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            bio=bio,
            cycle_length=cycle_length
        )
        user.set_password('Password123')
        user.save()

def seed_cycles():
    users = User.objects.all()
    """Create `num_cycles` number of cycles for the given `users`."""
    for user in users:
        cycle_length = user.cycle_length
        if cycle_length == 'WEEKLY':
            dates = past_weeks(20)
        elif cycle_length == 'MONTHLY':
            dates = past_months(5)
        for date in dates:
            Cycle.objects.create(
                user=user,
                start_date = date[0],
                cycle_length=cycle_length,
                accounts_session_date = date[2]
                )

def seed_template_categories():
    if not TemplateCategory.objects.exists():
        template_categories = [    
            {'name': 'Food & Drink', 'limit': 100.00},   
            {'name': 'Transportation', 'limit': 50.00}, 
            {'name': 'Entertainment', 'limit': 25.00},    
            {'name': 'Housing & Utilities', 'limit': 1000.00},    
            {'name': 'Health', 'limit': 150.00}
        ]
        for template_category in template_categories:
            TemplateCategory.objects.create(**template_category)

def seed_model_concrete_categories(): # default 2 category per user
    users = User.objects.all()
    all_template_categories = TemplateCategory.objects.all()
    for i in range(users.count()):
        user = users[i]
        template_category = all_template_categories[i%5]
        #create concrete categories from the template_categories
        ModelConcreteCategory.objects.create(
            current_name=template_category.name + f'{i}',
            user = user,
        )
        #create custom concrete categories
        ModelConcreteCategory.objects.create(
            current_name=f'Custom Category {i}',
            user = user,
        )

def seed_concrete_categories():
    users = User.objects.all()
    for user in users:
        model_categories = ModelConcreteCategory.objects.filter(user = user)
        cycles = Cycle.objects.filter(user=user).order_by('start_date')
        for model_category in model_categories:
            limit = randint(20, 2000)
            for index, cycle in enumerate(cycles):
                ConcreteCategory.objects.create(
                name=model_category.current_name + f'|{index}',
                user = model_category.user,
                limit=limit,
                cycle = cycle,
                model_concrete_category = model_category,
                goal_as_little_as_possible = choice([True, False]),
                goal_well_distributed = choice([True, False]),
                goal_x_less = randint(0, 10)
            )
        
def seed_spendings_in_the_monthly_cycle(num_spending_per_cycle = 3):
    fake = Faker()
    users = User.objects.all()
    for user in users:
        model_concrete_categories = ModelConcreteCategory.objects.filter(user=user)
        for mcc in model_concrete_categories:
            '''spendings name that will be consistently present in every cycle in this model concrete category.'''
            spending_name=[]
            for i in range(num_spending_per_cycle):
                spending_name += fake.word()
            concrete_categories = ConcreteCategory.objects.filter(user=user, model_concrete_category=mcc, cycle__cycle_length='MONTHLY').order_by('cycle__start_date')
            for concrete_category in concrete_categories:
                maximum_spending = (concrete_category.limit/num_spending_per_cycle) + 10
                for i in range(num_spending_per_cycle):
                    # Path to your photos folder
                    photos_folder = 'personal_spending_tracker/photos'

                    # Get a random file from the photos folder
                    photo_filename = random.choice(os.listdir(photos_folder))
                    photo_path = os.path.join(photos_folder, photo_filename)

                    # Copy the file to the Django media directory
                    shutil.copy(photo_path, os.path.join(MEDIA_ROOT, photo_filename))
                    
                    #Initialise is_regular fields and date field for use
                    CHOICES = [('monthly', 'Monthly'), ('yearly', 'Yearly')]
                    date = random_date(concrete_category.cycle.start_date,get_cycle_end_date(concrete_category.cycle))
                    is_regular = bool(random.getrandbits(1))
                    if is_regular:
                        frequency = random.choice([choice[0] for choice in CHOICES])
                        next_due_date = random_date(date, get_cycle_end_date(concrete_category.cycle))
                    else:
                        frequency = None
                        next_due_date = None
                    # Create the spending instance
                    Spending.objects.create(
                        title=spending_name[i],
                        date=date,
                        user = user,
                        amount=fake.pyfloat(min_value=0, max_value=maximum_spending, right_digits=2), 
                        description=fake.sentence(),
                        category = concrete_category,
                        photo=photo_filename,
                        is_regular=is_regular,
                        frequency=frequency,
                        next_due_date=next_due_date
                        )
                    
def seed_spendings_in_the_weekly_cycle(num_spending_per_cycle = 3):
    fake = Faker()
    users = User.objects.all()
    for user in users:
        model_concrete_categories = ModelConcreteCategory.objects.filter(user=user)
        for mcc in model_concrete_categories:
            '''spendings name that will be consistently present in every cycle in this model concrete category.'''
            spending_name=[]
            for i in range(num_spending_per_cycle):
                spending_name += fake.word()
            concrete_categories = ConcreteCategory.objects.filter(user=user, model_concrete_category=mcc, cycle__cycle_length='WEEKLY').order_by('cycle__start_date')
            for concrete_category in concrete_categories:
                maximum_spending = (concrete_category.limit/num_spending_per_cycle) + 10
                for i in range(num_spending_per_cycle):
                    # Path to your photos folder
                    photos_folder = 'personal_spending_tracker/photos'

                    # Get a random file from the photos folder
                    photo_filename = random.choice(os.listdir(photos_folder))
                    photo_path = os.path.join(photos_folder, photo_filename)

                    # Copy the file to the Django media directory
                    shutil.copy(photo_path, os.path.join(MEDIA_ROOT, photo_filename))

                    #Initialise is_regular fields and date field for use
                    CHOICES = [('monthly', 'Monthly'), ('yearly', 'Yearly')]
                    date = random_date(concrete_category.cycle.start_date,get_cycle_end_date(concrete_category.cycle))
                    is_regular = bool(random.getrandbits(1))
                    if is_regular:
                        frequency = random.choice([choice[0] for choice in CHOICES])
                        next_due_date = random_date(date, get_cycle_end_date(concrete_category.cycle))
                    else:
                        frequency = None
                        next_due_date = None
                    # Create the spending instance
                    Spending.objects.create(
                        title=spending_name[i],
                        date=date,
                        user = user,
                        amount=fake.pyfloat(min_value=0, max_value=maximum_spending, right_digits=2), 
                        description=fake.sentence(),
                        category = concrete_category,
                        photo=photo_filename,
                        is_regular=is_regular,
                        frequency=frequency,
                        next_due_date=next_due_date
                        )
                

def seed_points():
    users = User.objects.all()
    for user in users:
        model_concrete_categories = ModelConcreteCategory.objects.filter(user=user)
        for mcc in model_concrete_categories:
            concrete_categories = ConcreteCategory.objects.filter(user=user, model_concrete_category=mcc).order_by('cycle__start_date')
            previous_concrete_category = None
            for index, concrete_category in enumerate(concrete_categories):
                if index == 0:
                    if concrete_category.goal_as_little_as_possible:
                       spend_as_little_as_possible(concrete_category)
                    if concrete_category.goal_well_distributed:
                        well_distributed_spending(concrete_category)
                    complete_account_session_on_time(user)
                    not_exceeding_limit(concrete_category)
                    previous_concrete_category = concrete_category
                    continue
                if concrete_category.goal_as_little_as_possible:
                       spend_as_little_as_possible(concrete_category)
                if concrete_category.goal_well_distributed:
                    well_distributed_spending(concrete_category)
                if concrete_category.goal_x_less > 0:
                    compare_spending_from_previous_cycle(previous_concrete_category,concrete_category)
                complete_account_session_on_time(user)
                not_exceeding_limit(concrete_category)
                previous_concrete_category = concrete_category

"""Create user whose end_date is Today, to partake in the Account-Session."""
def seed_users_for_account_session():
    user_accounts = ["WEEKLY","MONTHLY"]
    for index, user_account in enumerate(user_accounts):
        username = f'user_account_session{index+1}' # user_account_session1 and user_account_session2 will be created.
        email = f'{username}@example.com'
        first_name = 'first_name'
        last_name = 'last_name'
        cycle_length = user_account
        date_of_birth = datetime.today() - timedelta(days=random.randint(16*365, 50*365))
        bio = ' '.join(['Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit.', 'Fusce', 'non', 'neque', 'vel', 'ligula', 'porttitor', 'interdum', 'ac', 'et', 'quam.', 'Donec', 'sodales', 'quam', 'in', 'ante', 'dignissim', 'tempus.'])
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            bio=bio,
            cycle_length=cycle_length
        )
        user.set_password('Password123')
        user.save()
        dates = past_weeks_from_today(8) if user.cycle_length == "WEEKLY" else past_months_from_today(2)
        for date in dates:
            Cycle.objects.create(
                user=user,
                start_date = date[0],
                cycle_length=cycle_length,
                accounts_session_date = date[2]
                )  


    