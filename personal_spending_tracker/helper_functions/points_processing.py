from personal_spending_tracker.models import *
from .views_time_frames import *
from decimal import Decimal

def spend_as_little_as_possible(concrete_category):
    spendings = Spending.objects.filter(category=concrete_category)
    total =0
    for spending in spendings:
        total+=spending.amount
    if total<=concrete_category.limit:
        calculation = (concrete_category.limit/total)*10 
        points_score = calculation if calculation<100 else 100
        PointReward.objects.create(
            cycle = concrete_category.cycle,
            points = points_score,
            rewarding_for = 'Increase in Savings',
            category = concrete_category   
            )
    
def not_exceeding_limit(concrete_category):
    spendings = Spending.objects.filter(category=concrete_category)
    total =0
    for spending in spendings:
        total+=spending.amount
    if total<concrete_category.limit:
        PointReward.objects.create(
            cycle = concrete_category.cycle,
            points = concrete_category.limit - total,
            rewarding_for = 'Spending as little as possible',
            category = concrete_category   
            )
    elif total>concrete_category.limit:
        PointReward.objects.create(
            cycle = concrete_category.cycle,
            points = concrete_category.limit - total,
            rewarding_for = 'Exceeded the budget_limit!',
            category = concrete_category   
            )
        
def well_distributed_spending(concrete_category):
    spendings = Spending.objects.filter(category=concrete_category)
    total =0
    for spending in spendings:
        total+=spending.amount
        spending_ratio = Decimal(total/concrete_category.limit)
        date_progression = Decimal(date_progression_through_cycle(concrete_category.cycle,spending.date))
        difference = round(abs(spending_ratio - date_progression),2)
        if  difference <= 0.1: 
            PointReward.objects.create(
            cycle = concrete_category.cycle,
            points = 10 - difference,
            rewarding_for = 'Well-distributed spending',
            category = concrete_category   
            )

def compare_spending_from_previous_cycle(previous_concrete_category,concrete_category):
    current_spendings = Spending.objects.filter(category=concrete_category)
    current_total =0
    previous_spendings = Spending.objects.filter(category=previous_concrete_category)
    previous_total =0
    for spending in current_spendings:
        current_total+=spending.amount
    for spending in previous_spendings:
        previous_total+=spending.amount
    if current_total< previous_total:
        saved_number = (previous_total-current_total/previous_total)*100
        saved= round(saved_number, 2)
        if saved>0:
            PointReward.objects.create(
                cycle = concrete_category.cycle,
                points = previous_total-current_total,
                rewarding_for = f'Cutting spending by {saved}% from previous cycle.',
                category = concrete_category   
                )
        elif saved<0: 
            PointReward.objects.create(
                cycle = concrete_category.cycle,
                points = previous_total-current_total,
                rewarding_for = f'Increased spending by {saved}% from previous cycle!',
                category = concrete_category   
                )

        
def complete_account_session_on_time(user):
    cycles = Cycle.objects.filter(user=user).order_by('start_date')
    for cycle in cycles:
        end_date = get_cycle_end_date(cycle)
        if cycle.accounts_session_date is not None:
            if not (cycle.accounts_session_date - end_date) > timedelta(days=1): #Account_Session did not exceed 1 day.
              PointReward.objects.create(
                cycle = cycle,
                points = 10,
                rewarding_for = 'Timely completion of the accounts session',
                category = None   
                )
            else: # Late Attendance of the Account_Session
                PointReward.objects.create(
                cycle = cycle,
                points = -1,
                rewarding_for = 'Timely completion of the accounts session',
                category = None   
                )



            
 