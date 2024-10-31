from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from datetime import datetime
from .seed_functions import *

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en-GB')

    def handle(self, *args, **options):
        seed_users()
        seed_cycles()
        seed_users_for_account_session()
        seed_template_categories()
        seed_model_concrete_categories()
        seed_concrete_categories()
        seed_spendings_in_the_weekly_cycle()
        seed_spendings_in_the_monthly_cycle()
        seed_points()
        
    