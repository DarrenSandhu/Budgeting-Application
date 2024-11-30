from django.core.management.base import BaseCommand, CommandError
from personal_spending_tracker.models import User

class Command(BaseCommand):
    help = 'Displays all users in the database'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            self.stdout.write(f"Username: {user.username}, Email: {user.email}, First Name: {user.first_name}, Last Name: {user.last_name}")