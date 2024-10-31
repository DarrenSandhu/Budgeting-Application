from datetime import date, timedelta
from calendar import monthrange
from ..models import *
from .views_time_frames import *
from .cycle_dates_computation import *
from .cycle_objects_retrieval_and_modification import *

def get_all_regular_spendings(request):
    cycle = get_active_cycle_for_user_HS(request.user)
    cycle_start_date = cycle.start_date
    cycle_end_date = get_cycle_end_date(cycle)

    all_regular_spendings = Spending.objects.filter(user_id = request.user.id,  is_regular=True, date__range=[cycle_start_date, cycle_end_date])
    return all_regular_spendings

def get_all_close_regular_spendings(request):
    all_regular_spendings = get_all_regular_spendings(request)
    # cycle = get_the_active_cycle_for_user(request.user)
    # cycle_end_date = get_cycle_end_date(cycle)
    all_close_spendings = []
    for spending in all_regular_spendings:
        today = spending.date
        nextDueDate = spending.next_due_date
        if ((nextDueDate - today).days) <= 3:
            all_close_spendings.append(spending)
    return all_close_spendings

def get_all_far_regular_spendings(request):
    all_regular_spendings = get_all_regular_spendings(request)
    # cycle = get_the_active_cycle_for_user(request.user)
    # cycle_end_date = get_cycle_end_date(cycle)
    all_far_spendings = []
    for spending in all_regular_spendings:
        today = spending.date
        nextDueDate = spending.next_due_date
        if ((nextDueDate - today).days) > 3:
            all_far_spendings.append(spending)
    return all_far_spendings