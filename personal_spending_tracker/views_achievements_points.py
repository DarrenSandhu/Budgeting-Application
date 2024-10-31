from django.shortcuts import render, redirect
from .helper_functions.filter_spendingAmount_by_category_date import *
from .models import Spending, ConcreteCategory, PointReward
from .helper_functions.views_time_frames import *
from .helper_functions.retrieve_active_cycle import *
from .helper_functions.points_processing import *
from .helper_functions.filter_points import *
from decimal import Decimal

def grade_points_for_active_cycle(request):

    previous,current=calculate_points_for_active_cycle_and_previous_cycle(request)
    
    if previous ==0:
        previous = max(current, 100)

    percentage = (current / previous) * 100
    
    if percentage >= 90:
        return percentage,"A+"
    elif percentage >= 80:
        return percentage,"A"
    elif percentage >= 70:
        return percentage,"B"
    elif percentage >= 60:
        return percentage,"C"
    elif percentage >= 50:
        return percentage,"D"
    elif percentage >= 40:
        return percentage, "E"
    else:
        return percentage,"F"

def calculate_points_for_active_cycle_and_previous_cycle(request):
    current_total=0
    previous_total=0
    reward_points_for_active_cycle(request)
    cycle=retrieve_the_active_cycle_for_user(request.user)
    prev_cycle = retrieve_the_previous_cycle_from_active_cycle(cycle)
    points = PointReward.objects.filter(user=request.user,cycle=cycle)
    prev_points = PointReward.objects.filter(user=request.user,cycle=prev_cycle) if prev_cycle is not None else 0
    for point in points:
        current_total+=point.points
    if prev_points !=0:
        for prev_point in prev_points:
            previous_total+=prev_point.points
    return previous_total, current_total

def reward_points_for_active_cycle(request):
    user = request.user
    cycle = retrieve_the_active_cycle_for_user(user)
    model_concrete_categories = ModelConcreteCategory.objects.filter(user=user)
    for mcc in model_concrete_categories:
        concrete_categories = ConcreteCategory.objects.filter(user=user, cycle = cycle,model_concrete_category=mcc).order_by('cycle__start_date')
        previous_concrete_category = None
        for index, concrete_category in enumerate(concrete_categories):
            if index == 0:
                if concrete_category.goal_as_little_as_possible:
                    spend_as_little_as_possible(concrete_category)
                if concrete_category.goal_well_distributed:
                    well_distributed_spending(concrete_category)
                complete_account_session_on_time(user)
                not_exceeding_limit(concrete_category)
                previous_concrete_category = concrete_category
                continue
            if concrete_category.goal_as_little_as_possible:
                spend_as_little_as_possible(concrete_category)
            if concrete_category.goal_well_distributed:
                well_distributed_spending(concrete_category)
            if concrete_category.goal_x_less > 0:
                compare_spending_from_previous_cycle(previous_concrete_category,concrete_category)
            complete_account_session_on_time(user)
            not_exceeding_limit(concrete_category)
            previous_concrete_category = concrete_category

def point_history(request, timefilter = "All", categoryfilter = "All"):
    current_user = request.user
    achievements = []
    categories = []
    no_of_achievements = 0

    # Retrieve all categories for user for filter dropdown
    for cat in ModelConcreteCategory.objects.filter(user_id=current_user.id).values():
        categories.append(cat.get("current_name"))
    categories.append("Cycle-Specific")
    # Display options for time filters
    time_options = ["Past Week", "This Week", "Past Month", "This Month", "Past Year", "This Year"]

    # Retrieve reward_title, points,  category, and session_date for each achievememt for the user
    if timefilter == "All" and categoryfilter == "All":
        achievements = all_points(request)
    elif categoryfilter == "All":
        if timefilter == "Past Week":
            achievements = all_points_in_past_week(request)
        elif timefilter == "This Week":
            achievements = all_points_in_this_week(request)
        elif timefilter == "Past Month":
            achievements = all_points_in_past_month(request)
        elif timefilter == "This Month":
            achievements = all_points_in_this_month(request)
        elif timefilter == "Past Year":
            achievements = all_points_in_past_year(request)
        elif timefilter == "This Year":
            achievements = all_points_in_this_year(request)
    elif timefilter == "All":
        achievements = all_points_for_category(request, categoryfilter)
    else:
        if timefilter == "Past Week":
            achievements = all_points_in_past_week_by_category(request, categoryfilter)
        elif timefilter == "This Week":
            achievements = all_points_in_this_week_by_category(request, categoryfilter)
        elif timefilter == "Past Month":
            achievements = all_points_in_past_month_by_category(request, categoryfilter)
        elif timefilter == "This Month":
            achievements = all_points_in_this_month_by_category(request, categoryfilter)
        elif timefilter == "Past Year":
            achievements = all_points_in_past_year_by_category(request, categoryfilter)
        elif timefilter == "This Year":
            achievements = all_points_in_this_year_by_category(request, categoryfilter)
    
    no_of_achievements = len(achievements)
    
    return render(request, 'point_history.html', { 'categoryfilter':categoryfilter, 'timefilter':timefilter, 'time_options':time_options, 'categories':categories, 'no_of_achievements':no_of_achievements, 'achievements':achievements})


    
'''Functions below compares spendings to their category limit in the given time frames'''  
    
def category_savings(request, category_id):
    total_spending =total_spendings_amount_in_chosen_category(request, category_id)
    category = ConcreteCategory.objects.get(id=category_id)
    limit = float(category.limit)
    amount = float(total_spending)
    difference = limit-amount
    if difference !=0:
        remaining = ((difference)/limit)*100
        remaining_rounded = round(remaining,2)
    else:
        remaining_rounded = 0

    return remaining_rounded

def category_savings_past_week(request, category_id, start_date=None, end_date=None):
    total_spending =total_spendings_amount_in_chosen_category_past_week(request, category_id,start_date, end_date)
    
    category = ConcreteCategory.objects.get(id=category_id)
    
    
    return float(category.limit) - float(total_spending)

def category_savings_past_month(request, category_id, start_date=None, end_date=None):
    total_spending =total_spendings_amount_in_chosen_category_past_month(request, category_id,start_date, end_date)
    
    category = ConcreteCategory.objects.get(id=category_id)
    
    return float(category.limit) - float(total_spending)

def category_savings_past_year(request, category_id, start_date=None, end_date=None):
    total_spending =total_spendings_amount_in_chosen_category_past_year(request, category_id,start_date, end_date)
    
    category = ConcreteCategory.objects.get(id=category_id)
    
    return float(category.limit) - float(total_spending)


