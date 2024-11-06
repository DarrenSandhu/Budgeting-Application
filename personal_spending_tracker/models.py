from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import date, datetime, timedelta
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

from .helper_functions.cycle_dates_computation import *

CYCLE_LENGTH_OPTIONS = (
    ('WEEKLY', 'weekly'),
    ('MONTHLY', 'monthly'),
)

REWARDING_FOR_OPTIONS = (
    ('A1', 'not exceeding category limit'),
    ('A2', 'timely completion of the accounts session'),
    ('B1', 'spending as little as possible'),
    ('B2', 'well-distributed spending'), 
    ('B3', 'cutting spending by x %'),
)

DEFAULT_USER = {
    "username" : "Unknown", 
    "email" : "unknown@u.com",
    "first_name" : "Un",
    "last_name" : "Known",
    "cycle_length" : "MONTHLY",
}

DEFAULT_CONCRETE_CATEGORY = {
    "name" : "Uncategorised",
    "limit" : 100,
}

def get_user_id():
    user, _ = User.objects.get_or_create(username=DEFAULT_USER["username"], email=DEFAULT_USER["email"], first_name=DEFAULT_USER["first_name"], last_name=DEFAULT_USER["last_name"], cycle_length=DEFAULT_USER["cycle_length"])
    return user.id

def get_cycle_id():
    user, _ = User.objects.get_or_create(username=DEFAULT_USER["username"], email=DEFAULT_USER["email"], first_name=DEFAULT_USER["first_name"], last_name=DEFAULT_USER["last_name"], cycle_length=DEFAULT_USER["cycle_length"])
    # cycle, _ = Cycle.objects.get_or_create(user=user)
    # return cycle.id
    cycle = Cycle.objects.filter(user=user).order_by('-start_date').first()
    return cycle.id if cycle else None

def get_model_concrete_category_id():
    user, _ = User.objects.get_or_create(username=DEFAULT_USER["username"], email=DEFAULT_USER["email"], first_name=DEFAULT_USER["first_name"], last_name=DEFAULT_USER["last_name"], cycle_length=DEFAULT_USER["cycle_length"])
    # model_concrete_category, _ = ModelConcreteCategory.objects.get_or_create(user=user)
    try:
        model_concrete_category = Cycle.objects.filter(user=user)[0]
    except:
        return None
    return model_concrete_category.id if model_concrete_category else None

# there is some sort of problem with this function 
def get_concrete_category_id():
    user, _ = User.objects.get_or_create(username=DEFAULT_USER["username"], email=DEFAULT_USER["email"], first_name=DEFAULT_USER["first_name"], last_name=DEFAULT_USER["last_name"], cycle_length=DEFAULT_USER["cycle_length"])
    model_concrete_category, _ = ModelConcreteCategory.objects.get_or_create(user=user)
    cycle, _ = Cycle.objects.get_or_create(user=user)

    concrete_category, _ = ConcreteCategory.objects.get_or_create(name=DEFAULT_CONCRETE_CATEGORY['name'], limit=DEFAULT_CONCRETE_CATEGORY['limit'], user=user, cycle=cycle, model_concrete_category=model_concrete_category)
    return concrete_category.id

class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True, null=False, blank=False,
        validators=[RegexValidator(
            regex=r'^.{5,}$',
            message='Username must contain at least 5 characters'
        )]
    )
    email = models.EmailField(unique=True, null=False, blank=False,
        validators=[EmailValidator(
            message="Please enter a valid email address"
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.TextField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    cycle_length = models.CharField(choices=CYCLE_LENGTH_OPTIONS, max_length=50, null=False, blank=False, default='MONTHLY')
    #objects = PersonalSpendingTrackerUserManager()

class TemplateCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    limit = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.name
    
class Cycle(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=get_user_id)
    # should be back to back with the previous cycle's completion 
    # there should run a function checking if the previoysly active cycle has expired and if so create a new one with the date following the previous one's completion
    # because of how Cycles are created the default will not ever get used, but maybe it shoudl get changed anyway to something reflective of what the default start dates could be? 
    start_date = models.DateField(default=date.today, null=False, blank=False)
    cycle_length = models.CharField(choices=CYCLE_LENGTH_OPTIONS, max_length=50, null=False, blank=False, default='MONTHLY')
    # this only gets filled in once the user completes the session 
    accounts_session_date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.accounts_session_date:
            if not (self.start_date <= self.accounts_session_date <= get_last_cycle_date(self.start_date, self.cycle_length)): 
                raise ValidationError('The date of the accounts session is not within the cycle. If a cycle has passed, completing an accounts session is not allowed.')
            #TODO: should there be a validator for the cycle_length being the same as the user's cycle_length? Will it not mess the DB up retrospectively? When is the clean() method called? Only when an object is created/ edited?

class ModelConcreteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=get_user_id)
    current_name = models.CharField(max_length=100)
    class Meta:
        unique_together = (("user", "current_name"),)
    def __str__(self):
        return self.current_name


class ConcreteCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    limit = models.IntegerField(null=False, blank=False, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=get_user_id)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, blank=False, null=False, default=get_cycle_id)
    model_concrete_category = models.ForeignKey(ModelConcreteCategory, on_delete=models.CASCADE, blank=False, null=False, default=get_model_concrete_category_id, related_name='category')
    # goals 
    goal_as_little_as_possible = models.BooleanField(default=False)
    goal_well_distributed = models.BooleanField(default=False)
    goal_x_less = models.IntegerField(default=0)

    class Meta:
        unique_together = (("user", "name", "cycle"),)


    def __str__(self):
        return self.name

    def clean(self):
        if self.cycle.user != self.user: # TODO: + limit choice - FORMS?
            raise ValidationError('The user of the cycle must be the same as the user of the ConcreteCategory.')
        if self.model_concrete_category.user != self.user: #TODO: + limit choice - FORMS?
            raise ValidationError('The user of the model concrete category must be the same as the user of the ConcreteCategory.')
        
class Spending(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(default=date.today, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='media', blank=True)
    is_regular = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly','Yearly')], blank=True, null=True)
    next_due_date = models.DateField(null=True, blank=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=get_user_id)
    #TODO: non-nullablle 
    category = models.ForeignKey(ConcreteCategory, on_delete=models.CASCADE)

    def clean(self):
        if self.category.user != self.user:
            raise ValidationError('The user of the category assigned must be the same as the user of the spending object.')
        if self.date < self.category.cycle.start_date or self.date > get_last_cycle_date(self.category.cycle):
            raise ValidationError('The date assigned to the spending is not within the current cycle, i.e. ' + self.category.cycle.start_date.strftime('%d-%m-%Y') + ' to ' + get_last_cycle_date(self.category.cycle).strftime('%d-%m-%Y'))
        # TODO: category - limit choice by user, limit choice by current_cycle - FORMS?
    

class PointReward(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, blank=False, null=False, default=get_cycle_id)
    points = models.IntegerField(null=False, blank=False)
    rewarding_for = models.CharField(choices=REWARDING_FOR_OPTIONS, max_length=50, null=False, blank=False)
    # TODO: category - limit choice by user from the cycle - FORMS?
    category = models.ForeignKey(ConcreteCategory, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.category.user != self.cycle.user:
            raise ValidationError('The user of the category assigned must be the same as the user of the cycle assigned.')
        








