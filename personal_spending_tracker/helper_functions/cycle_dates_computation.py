from datetime import datetime, timedelta
import calendar
from multipledispatch import dispatch

# return: first DATE past a cycle
def get_first_expiration_date_for_cycle_HS(cycle):
    if cycle.cycle_length == "WEEKLY": 
        return cycle.start_date + timedelta(days=7) 
    elif cycle.cycle_length == "MONTHLY":
        next_month_date = cycle.start_date + timedelta(days=31)
        return next_month_date
    else: 
        raise ValueError("The cycle's length is invalid.")
    
# return: first DATE past a cycle
def get_first_expiration_date_for_cycle(cycle):
    if cycle.cycle_length == "WEEKLY": 
        return cycle.start_date + timedelta(days=7) 
    elif cycle.cycle_length == "MONTHLY":
        next_month_date = cycle.start_date + timedelta(days=31)
        return next_month_date.replace(day=1) 
    else: 
        raise ValueError("The cycle's length is invalid.")
    
# return: last DATE of a cycle (parameter: cycle)
@dispatch(object)
def get_last_cycle_date(cycle):
    if (cycle.cycle_length == "WEEKLY"):
        first_date_following_cycle = cycle.start_date + timedelta(days=7)
    elif(cycle.cycle_length == "MONTHLY"):
        cycle_month = cycle.start_date.month 
        first_date_following_cycle = cycle.start_date.replace(month=cycle_month+1)
    else: 
        raise ValueError("The cycle's length is invalid.")

    return first_date_following_cycle - timedelta(days=1)

# return: last DATE of a cycle (parameters: start_date, cycle_length)
@dispatch(object, object)
def get_last_cycle_date(start_date, cycle_length):
    if (cycle_length == "WEEKLY"):
        first_date_following_cycle = start_date + timedelta(days=7)
    elif(cycle_length == "MONTHLY"):
        cycle_month = start_date.month 
        first_date_following_cycle = start_date.replace(month=cycle_month+1)
    else: 
        raise ValueError("The cycle's length is invalid.")

    return first_date_following_cycle - timedelta(days=1)

# return: NUMBER - cycle duration 
def get_number_of_days_for_cycle(cycle):
    if (cycle.cycle_length == "MONTHLY"): 
        return calendar.monthrange(cycle.start_date.year, cycle.start_date.month)[1]
    elif (cycle.cycle_length == "WEEKLY"):
        return 7
    else: 
        raise ValueError("The cycle's length is invalid.")
    




    
    
    