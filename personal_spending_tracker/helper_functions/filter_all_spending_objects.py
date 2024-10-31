from datetime import datetime, timedelta
from calendar import monthrange

from personal_spending_tracker.helper_functions.cycle_objects_retrieval_and_modification import *
from ..models import *
from .views_time_frames import *

def all_spendings(request):
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_for_active_cycle(request):
    active_cycle = get_active_cycle_for_user_HS(user = request.user)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id):
            category = ConcreteCategory.objects.get(id=each.category.id)
            if category.cycle == active_cycle:
                newSpending = [each,category]
                transactions.append(newSpending)
    return transactions

def all_spendings_for_category(request, category_name):
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id):
                category = ConcreteCategory.objects.filter(id=each.category.id).first()
                newSpending = [each,category]
                transactions.append(newSpending)
    return transactions

def all_spendings_in_past_week(request, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_week(request, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_month(request, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_month(request, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_year(request, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_year(request, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions


#_________________________________________________________________________________________________________________________

def all_spendings_in_past_week_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id, date__range=(start_date, end_date)):
                category = ConcreteCategory.objects.filter(id=each.category.id).first()
                newSpending = [each,category]
                transactions.append(newSpending)
    return transactions

def all_spendings_in_this_week_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id, date__range=(start_date, end_date)):
                category = ConcreteCategory.objects.filter(id=each.category.id).first()
                newSpending = [each,category]
                transactions.append(newSpending)
    return transactions

def all_spendings_in_past_month_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id, date__range=(start_date, end_date)):
                category = ConcreteCategory.objects.filter(id=each.category.id).first()
                newSpending = [each,category]
                transactions.append(newSpending)
    return transactions

def all_spendings_in_this_month_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_year_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_year_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    model_category = ModelConcreteCategory.objects.get(current_name=category_name)
    categories =  ConcreteCategory.objects.filter(model_concrete_category=model_category)
    transactions = []
    for category in categories:
        for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

#_________________________________________________________________________________________________________________________
# by MODEL Concrete Category 
def all_spendings_for_model_category(request, category_name):
    model_category = ModelConcreteCategory.objects.filter(user=request.user).get(current_name=category_name)

    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category=model_category):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_week_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_week_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_month_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_month_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_year_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_year_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)):
            category = ConcreteCategory.objects.filter(id=each.category.id).first()
            newSpending = [each,category]
            transactions.append(newSpending)
    return transactions
