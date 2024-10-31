from ..models import ConcreteCategory, Spending
from .filter_all_spending_objects import *
import numpy as np
import math
import json
from .json_processing import *
from .cycle_objects_retrieval_and_modification import * 
from .cycle_dates_computation import *
from .spending_retrieval import *
from .CC_MCC_objects_retrieval import *
from personal_spending_tracker.forms import EditSpendingForm
from budgeting_app.settings import MEDIA_ROOT, MEDIA_URL

def fetch_context_for_spending_history_data_objects(request, timefilter = "All", categoryfilter = "All", cyclefilter = "Current"):
    current_user = request.user
    transactions = []
    categories = get_active_model_concrete_categories(current_user)
    no_of_transactions = 0

    # Retrieve all categories for user for filter dropdown
    # for cat in ModelConcreteCategory.objects.filter(user=current_user):
    #     categories.append(cat)
    
    # Display options for time filters
    time_options = ["Past Week", "This Week", "Past Month", "This Month", "Past Year", "This Year"]

    # Retrieve title, desc, amount, category, photo and date for chosen transactions for user
    if timefilter == "All" and categoryfilter == "All":
        transactions = all_spendings(request)
    elif timefilter == "Cycle":
        transactions = all_spendings_for_active_cycle(request)
    elif categoryfilter == "All":
        if timefilter == "Past Week":
            transactions = all_spendings_in_past_week(request)
        elif timefilter == "This Week":
            transactions = all_spendings_in_this_week(request)
        elif timefilter == "Past Month":
            transactions = all_spendings_in_past_month(request)
        elif timefilter == "This Month":
            transactions = all_spendings_in_this_month(request)
        elif timefilter == "Past Year":
            transactions = all_spendings_in_past_year(request)
        elif timefilter == "This Year":
            transactions = all_spendings_in_this_year(request)
    elif timefilter == "All":
        transactions = all_spendings_for_category(request, categoryfilter)
    else:
        if timefilter == "Past Week":
            transactions = all_spendings_in_past_week_by_category(request, categoryfilter)
        elif timefilter == "This Week":
            transactions = all_spendings_in_this_week_by_category(request, categoryfilter)
        elif timefilter == "Past Month":
            transactions = all_spendings_in_past_month_by_category(request, categoryfilter)
        elif timefilter == "This Month":
            transactions = all_spendings_in_this_month_by_category(request, categoryfilter)
        elif timefilter == "Past Year":
            transactions = all_spendings_in_past_year_by_category(request, categoryfilter)
        elif timefilter == "This Year":
            transactions = all_spendings_in_this_year_by_category(request, categoryfilter)
    
    no_of_transactions = len(transactions)

    spendings = Spending.objects.filter(user_id=current_user.id)

    frequencies = [choice[0] for choice in Spending._meta.get_field('frequency').choices]

    cycle = get_active_cycle_for_user_HS(user=request.user)
    last_cycle_date = get_last_cycle_date(cycle)
    first_cycle_date = cycle.start_date

    context = { 
        'categoryfilter': categoryfilter, 
        'timefilter':timefilter, 
        'cyclefilter' : cyclefilter,
        'time_options': time_options, 
        'categories':categories, 
        'no_of_transactions':no_of_transactions, 
        'transactions':transactions,
        'spendings': spendings,
        'frequency': frequencies,
        'last_cycle_date': last_cycle_date,
        'first_cycle_date': first_cycle_date,
        'cycle': cycle,
        'MEDIA_URL': MEDIA_URL
        }
    
    return context