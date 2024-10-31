from datetime import datetime, timedelta
from calendar import monthrange
from ..models import *
from .views_time_frames import *

def spendings_in_chosen_category(user, category_id):
    spendings = Spending.objects.filter(user=user, category_id=category_id)
    return spendings

def spendings_in_chosen_category_past_week(request, category_id,start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    spendings = Spending.objects.filter(user=request.user, category_id=category_id, date__range=(start_date, end_date))
    return spendings

def spendings_in_chosen_category_this_week(request, category_id,start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    spendings = Spending.objects.filter(user=request.user, category_id=category_id, date__range=(start_date, end_date))
    return spendings

def spendings_in_chosen_category_past_month(request, category_id,start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    spendings = Spending.objects.filter(user=request.user, category_id=category_id, date__range=(start_date, end_date))
    return spendings

def spendings_in_chosen_category_this_month(request, category_id,start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    spendings = Spending.objects.filter(user=request.user, category_id=category_id, date__range=(start_date, end_date))
    return spendings

def spendings_in_chosen_category_past_year(request, category_id,start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    spendings = Spending.objects.filter(user=request.user, category_id=category_id, date__range=(start_date, end_date))
    return spendings

def spendings_in_chosen_category_this_year(request, category_id,start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    spendings = Spending.objects.filter(user=request.user, category_id=category_id, date__range=(start_date, end_date))
    return spendings
