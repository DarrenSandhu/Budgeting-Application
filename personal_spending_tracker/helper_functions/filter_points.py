from datetime import datetime, timedelta
from calendar import monthrange

from personal_spending_tracker.helper_functions.cycle_objects_retrieval_and_modification import *
from ..models import *
from .views_time_frames import *

def all_points(request): 
    achievements = []
    cycles = Cycle.objects.filter(user_id=request.user.id).exclude(accounts_session_date=None)
    for cycle in cycles:
        points = PointReward.objects.filter(cycle=cycle)
        for point in points:
            category = point.category
            if category is None:
                category_name = "Cycle-Specific"
            else:
                category_name = category.model_concrete_category.current_name
            newPoint = [point.rewarding_for, point.points, category_name, cycle.accounts_session_date]
            achievements.append(newPoint)
    return achievements

def all_points_for_active_cycle(request): 
    achievements = []
    active_cycle = get_active_cycle_for_user_HS(user = request.user)
    points = PointReward.objects.filter(cycle=active_cycle)
    for point in points:
        category = point.category
        if category is None:
            category_name = "Cycle-Specific"
        else:
            category_name = category.model_concrete_category.current_name
        newPoint = [point.rewarding_for, point.points, category_name, active_cycle.accounts_session_date]
        achievements.append(newPoint)
    return achievements

def all_points_for_category(request, category_name):
    achievements = []
    cycles = Cycle.objects.filter(user_id=request.user.id).exclude(accounts_session_date=None)
    for cycle in cycles:
        points = PointReward.objects.filter(cycle=cycle)
        for point in points:
            category = point.category
            if category is None :
                if category_name =="Cycle-Specific":
                    newPoint = [point.rewarding_for, point.points, category_name, cycle.accounts_session_date]
                    achievements.append(newPoint)
            elif category.model_concrete_category.current_name == category_name:
                newPoint = [point.rewarding_for, point.points, category_name, cycle.accounts_session_date]
                achievements.append(newPoint)
    return achievements 

def all_points_in_this_time_frame(request,start_date, end_date):
    achievements = []
    cycles = Cycle.objects.filter(user_id=request.user.id, accounts_session_date__range=[start_date, end_date],).exclude(accounts_session_date=None)
    for cycle in cycles:
        points = PointReward.objects.filter(cycle=cycle)
        for point in points:
            category = point.category
            if category is None:
                category_name = "Cycle-Specific"
            else:
                category_name = category.model_concrete_category.current_name
            newPoint = [point.rewarding_for, point.points, category_name, cycle.accounts_session_date]
            achievements.append(newPoint)
    return achievements

def all_points_in_past_week(request, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    return all_points_in_this_time_frame(request,start_date, end_date)

def all_points_in_this_week(request, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    return all_points_in_this_time_frame(request,start_date, end_date)

def all_points_in_past_month(request, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    return all_points_in_this_time_frame(request,start_date, end_date)

def all_points_in_this_month(request, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    return all_points_in_this_time_frame(request,start_date, end_date)

def all_points_in_past_year(request, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    return all_points_in_this_time_frame(request,start_date, end_date)

def all_points_in_this_year(request, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    return all_points_in_this_time_frame(request,start_date, end_date)
#_________________________________________________________________________________________________________________________
def all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date):
    achievements = []
    cycles = Cycle.objects.filter(user_id=request.user.id, accounts_session_date__range=[start_date, end_date],).exclude(accounts_session_date=None)
    for cycle in cycles:
        points = PointReward.objects.filter(cycle=cycle)
        for point in points:
            category = point.category
            if category is None :
                if category_name =="Cycle-Specific":
                    newPoint = [point.rewarding_for, point.points, category_name, cycle.accounts_session_date]
                    achievements.append(newPoint)
            elif category.model_concrete_category.current_name == category_name:
                newPoint = [point.rewarding_for, point.points, category_name, cycle.accounts_session_date]
                achievements.append(newPoint)
    return achievements

def all_points_in_past_week_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    return  all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date) 

def all_points_in_this_week_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    return  all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date)

def all_points_in_past_month_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    return all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date)

def all_points_in_this_month_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    return all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date)

def all_points_in_past_year_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    return  all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date)

def all_points_in_this_year_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    return all_points_in_this_time_frame_by_category(request, category_name,start_date, end_date)
