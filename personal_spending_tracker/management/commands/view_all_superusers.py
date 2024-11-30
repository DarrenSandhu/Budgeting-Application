from django.core.management.base import BaseCommand
from personal_spending_tracker.models import User

class Command(BaseCommand):
    help = 'Lists all superusers'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            self.stdout.write(f"Username: {user.username}, Email: {user.email}")
