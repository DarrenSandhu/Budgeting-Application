from datetime import datetime, timedelta
from calendar import monthrange
import random
from dateutil.relativedelta import relativedelta

'''This Week(from monday) or enter a specified custom time-frame'''
def this_week(start_date=None, end_date=None):
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=datetime.now().weekday())
    elif start_date and not end_date:
         start_date = start_date - timedelta(days=start_date.weekday()) # Monday
    if not end_date:
        end_date = start_date + timedelta(days=6)
        
    return (start_date, end_date)

'''Past Week (e.g if today is wednesday, then last wednesday to today) 
    or enter a specified custom time-frame'''
def past_week(start_date=None, end_date=None):
    if not end_date:
        end_date = datetime.now().replace(hour=0, minute=0, second=0)
    if not start_date:
        start_date = end_date - timedelta(days=7)
        
    return (start_date, end_date)

'''Returns the date of next week'''    
def next_week(start_date=None):
    if not start_date:
        start_date = datetime.today()
    end_date = start_date + timedelta(days=6) 
    return end_date

'''This Month(first day of the current month) or enter a specified custom time-frame'''
def this_month(start_date=None, end_date=None):
    if not start_date:
        start_date = datetime.now().replace(day=1) #1st day of the current month.
    elif start_date and not end_date: # 1st day of the "start_dates's" month
        start_date = start_date.replace(day=1)
    if not end_date:
        last_day = monthrange(start_date.year, start_date.month)[1]
        end_date = start_date.replace(day=last_day)
    return (start_date, end_date)

'''Past Month or enter a specified custom time-frame'''
def past_month(start_date=None, end_date=None):
    if not end_date:
        end_date = datetime.now().replace(hour=0, minute=0, second=0)
    if not start_date:
        last_day = monthrange(end_date.year, end_date.month)[1]
        start_date = end_date.replace(day=1) - timedelta(days=last_day - 1)
        if start_date.day > end_date.day:
            start_date = start_date.replace(day=end_date.day)
    return (start_date, end_date)

'''Returns the date of next month'''  
def next_month(start_date=None): #only returns the end date
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0)

    end_month = (start_date.month % 12) + 1  # Add 1 month, wrapping to January if necessary
    end_year = start_date.year + (1 if end_month == 1 else 0)  # Add 1 year if we wrap to January
    end_day = min(start_date.day, (datetime(end_year, end_month, 1) - timedelta(days=1)).day)  # Keep the same day if possible
    end_date = datetime(end_year, end_month, end_day, hour=0, minute=0, second=0)

    return end_date

'''This Year(first day of the first month of this year) 
    or enter a specified custom time-frame'''
def this_year(start_date=None, end_date=None):
    if not start_date:
        start_date = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0)
        
    if not end_date:
        end_date = start_date.replace(month=12, day=31)
        
    return (start_date, end_date)

'''Past Year or enter a specified custom time-frame'''
def past_year(start_date=None, end_date=None):
    if not end_date:
        end_date = datetime.now().replace(hour=0, minute=0, second=0)
    if not start_date:
        start_date = end_date.replace(month=1, day=1) - timedelta(days=365)
    return (start_date, end_date)

def past_months(num_months):
    months = []
    start_date, end_date = this_month()
    for i in range(num_months):
        if i ==0:
            session = end_date + timedelta(days=random.randint(0, 1))
            months.append((start_date, end_date,session))
        else:
            date = start_date - timedelta(days=1)
            start_date , end_date = this_month(start_date=date)
            session = end_date + timedelta(days=random.randint(0,1))
            months.append((start_date, end_date,session))
    return months

def past_weeks(num_weeks):
    weeks = []
    start_date, end_date = this_week()
    for i in range(num_weeks):
        if i ==0:
            session = end_date + timedelta(days=random.randint(0, 1))
            weeks.append((start_date, end_date,session))
        else:
            date = start_date - timedelta(days=1)
            start_date , end_date = this_week(start_date=date)
            session = end_date + timedelta(days=random.randint(0, 1))
            weeks.append((start_date, end_date,session))
    return weeks

def past_months_from_today(num_months):
    months = []
    start_date, end_date = past_month(end_date=datetime.now())
    for i in range(num_months):
        if i ==0:
            session = end_date
            months.append((start_date, end_date,session))
        else:
            start_date , end_date = past_month(end_date=start_date)
            session = end_date + timedelta(days=random.randint(0,1))
            months.append((start_date, end_date,session))
    return months

def past_weeks_from_today(num_weeks):
    weeks = []
    start_date, end_date = past_week(end_date=datetime.now())
    for i in range(num_weeks):
        if i ==0:
            session = end_date 
            weeks.append((start_date, end_date,session))
        else:
            start_date , end_date = past_week(end_date=start_date)
            session = end_date + timedelta(days=random.randint(0, 1))
            weeks.append((start_date, end_date,session))
    return weeks

def random_date(start_date, end_date):
    delta = (end_date - start_date).days +1
    random_days = random.randint(0, delta)
    return start_date + timedelta(days=random_days)

# return: end DATE of a cycle (parameter: cycle)
def get_cycle_end_date(cycle):
    if (cycle.cycle_length == "WEEKLY"):
        end_date = this_week(start_date=cycle.start_date)[1]
    elif(cycle.cycle_length == "MONTHLY"):
        end_date = this_month(start_date=cycle.start_date)[1]
    else: 
        raise ValueError("The cycle's length is invalid.")

    return end_date

def date_progression_through_cycle(cycle, todays_date=None):
    today = todays_date if todays_date is not None else datetime.now()
    if (cycle.cycle_length == "WEEKLY"):
        start_date, end_date = this_week(todays_date)
        total_cycle = relativedelta(end_date,start_date).days +1
    elif(cycle.cycle_length == "MONTHLY"):
        start_date, end_date = this_month(todays_date)
        total_cycle = relativedelta(end_date,start_date).days +1
    if total_cycle != 0:
        return today.day / total_cycle
    else:
        raise ValueError(f"The cycle's length is invalid. end_date - start_date = {end_date}-{start_date}")