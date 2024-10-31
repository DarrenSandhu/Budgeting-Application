from ..models import *
from datetime import datetime, timedelta
from .views_time_frames import next_month


def obtain_first_expiration_date_for_cycle(cycle):
    if cycle.cycle_length == "WEEKLY": 
        return cycle.start_date + timedelta(days=7) 
    elif cycle.cycle_length == "MONTHLY":
        return  next_month(cycle.start_date)


def retrieve_the_active_cycle_for_user(user):
    all_users_cycles = Cycle.objects.filter(user=user)
    
    for cycle in all_users_cycles: 
        if obtain_first_expiration_date_for_cycle(cycle) > datetime.now(): #end_date not reached yet
            return cycle     
    raise Exception("Active cycle not found!")

def retrieve_the_previous_cycle_from_active_cycle(active_cycle):
    all_users_cycles = Cycle.objects.filter(user=active_cycle.user)
    
    for prev_cycle in all_users_cycles: 
        if obtain_first_expiration_date_for_cycle(prev_cycle) == active_cycle.start_date: 
            return prev_cycle     
    return None