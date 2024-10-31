from ..models import Cycle, Spending
from datetime import datetime, timedelta
from .cycle_dates_computation import *

# return: Cycle DB object 
# it might need to also check for the number of active cycles found, just in case 
def get_the_active_cycle_for_user(user):
    all_user_cycles = Cycle.objects.filter(user=user).order_by('-start_date')  
    for cycle in all_user_cycles: 
        if get_first_expiration_date_for_cycle(cycle) > datetime.today().date(): 
            return cycle     
    return None

# return: Cycle DB object 
def get_active_cycle_for_user_HS(user):
    all_user_cycles = Cycle.objects.filter(user=user).order_by('-start_date')
    if len(all_user_cycles) >= 1: 
        return all_user_cycles[0]
    return None

# return: Cycle DB object 
def get_the_most_recent_cycle(user):
    all_user_cycles = Cycle.objects.filter(user=user).order_by('-start_date')
    if len(all_user_cycles) >= 1: 
        return all_user_cycles[0]
    return None

# return: Cycle DB object 
def get_previous_active_cycle_for_user(user):
    all_user_cycles = Cycle.objects.filter(user=user).order_by('-start_date')
    if len(all_user_cycles) >= 2: 
        return all_user_cycles[1]
    return None

# modifier function 
def ensure_an_active_cycle(user): 
    if get_the_active_cycle_for_user(user): 
        return 
    else: 
        if user.cycle_length == "MONTHLY": 
            start_date = datetime.today().replace(day=1)
            Cycle.objects.create(user=user, start_date=start_date, cycle_length="MONTHLY")
        else:
            deltatime_since_most_recent_monday = (datetime.today().weekday() - 0) % 7
            most_recent_monday = datetime.today() - timedelta(days=deltatime_since_most_recent_monday)
            start_date = most_recent_monday 
            Cycle.objects.create(user=user, start_date=start_date, cycle_length="WEEKLY")
    return 

# return: Spendings QuerySet
# without cycle argument to get current cycle's spendings
def get_cycle_spendings(user, cycle = None):
    if cycle:
        spendings = Spending.objects.filter(category__cycle=cycle)
    else:
        current_cycle = get_the_active_cycle_for_user(user)
        spendings = Spending.objects.filter(category__cycle=current_cycle)
    return spendings

# return: NUMBER
def get_current_cycle_number_of_days(user):
    current_cycle = get_the_active_cycle_for_user(user)
    return get_number_of_days_for_cycle(current_cycle)

# return: string
def get_cycle_timeframe_string_o_cycle(user, cycle = None):
    if not cycle: 
        cycle = get_the_active_cycle_for_user(user)
    start_date = cycle.start_date
    end_date = get_last_cycle_date(cycle)
    return start_date.strftime('%d-%m-%Y') + ' to ' + end_date.strftime('%d-%m-%Y')
