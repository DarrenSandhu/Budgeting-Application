from django.core.management.base import BaseCommand, CommandError
from personal_spending_tracker.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        Cycle.objects.all().delete()
        TemplateCategory.objects.all().delete()
        ModelConcreteCategory.objects.all().delete()
        ConcreteCategory.objects.all().delete()
        Spending.objects.all().delete()
        PointReward.objects.all().delete()