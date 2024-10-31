from datetime import datetime, timedelta
from calendar import monthrange
from ..models import *
from .filter_spending_by_category_date import *

def total_spendings_amount_in_chosen_category(user, category_id):
    spendings = spendings_in_chosen_category(user, category_id)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

def total_spendings_amount_in_chosen_category_past_week(request, category_id, start_date=None, end_date=None):
    spendings = spendings_in_chosen_category_past_week(request, category_id,start_date, end_date)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

def total_spendings_amount_in_chosen_category_this_week(request, category_id, start_date=None, end_date=None):
    spendings = spendings_in_chosen_category_this_week(request, category_id,start_date, end_date)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

def total_spendings_amount_in_chosen_category_past_month(request, category_id, start_date=None, end_date=None):
    spendings = spendings_in_chosen_category_past_month(request, category_id,start_date, end_date)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

def total_spendings_amount_in_chosen_category_this_month(request, category_id, start_date=None, end_date=None):
    spendings = spendings_in_chosen_category_this_month(request, category_id,start_date, end_date)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

def total_spendings_amount_in_chosen_category_past_year(request, category_id, start_date=None, end_date=None):
    spendings = spendings_in_chosen_category_past_year(request, category_id,start_date, end_date)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

def total_spendings_amount_in_chosen_category_this_year(request, category_id, start_date=None, end_date=None):
    spendings = spendings_in_chosen_category_this_year(request, category_id,start_date, end_date)
    total_spending = 0
    for spending in spendings:
        total_spending += spending.amount
    
    return total_spending

