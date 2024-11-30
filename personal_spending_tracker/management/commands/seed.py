from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from datetime import datetime
from .seed_functions import *

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en-GB')

    def handle(self, *args, **options):
        # Print a message indicating the start of the seeding process
        print("Starting the seeding process...")

        # Seeding Users
        print("Seeding users...")
        seed_users()
        print("Finished seeding users.")

        # Seeding Cycles
        print("Seeding cycles...")
        seed_cycles()
        print("Finished seeding cycles.")

        # Seeding Users for Account Session
        print("Seeding users for account sessions...")
        seed_users_for_account_session()
        print("Finished seeding users for account sessions.")

        # Seeding Template Categories
        print("Seeding template categories...")
        seed_template_categories()
        print("Finished seeding template categories.")

        # Seeding Model Concrete Categories
        print("Seeding model concrete categories...")
        seed_model_concrete_categories()
        print("Finished seeding model concrete categories.")

        # Seeding Concrete Categories
        print("Seeding concrete categories...")
        seed_concrete_categories()
        print("Finished seeding concrete categories.")

        # Seeding Spendings in Weekly Cycle
        print("Seeding spendings in the weekly cycle...")
        seed_spendings_in_the_weekly_cycle()
        print("Finished seeding spendings in the weekly cycle.")

        # Seeding Spendings in Monthly Cycle
        print("Seeding spendings in the monthly cycle...")
        seed_spendings_in_the_monthly_cycle()
        print("Finished seeding spendings in the monthly cycle.")

        # Seeding Points
        print("Seeding points...")
        seed_points()
        print("Finished seeding points.")

        # Print a message indicating the end of the seeding process
        print("Seeding process completed.")
        
        
    