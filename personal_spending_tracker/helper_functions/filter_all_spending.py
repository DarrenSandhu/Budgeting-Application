from datetime import datetime, timedelta
from calendar import monthrange

from personal_spending_tracker.helper_functions.cycle_objects_retrieval_and_modification import *
from ..models import *
from .views_time_frames import *

def all_spendings(request):
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_for_active_cycle(request):
    active_cycle = get_active_cycle_for_user_HS(user = request.user)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id).values():
            category = ConcreteCategory.objects.get(id=each.get("category_id"))
            if category.cycle == active_cycle:
                newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
                transactions.append(newSpending)
    return transactions

def all_spendings_for_category(request, category_name):
    category = ConcreteCategory.objects.get(name=category_name)

    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category_id=category.id).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_week(request, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_week(request, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_month(request, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_month(request, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_year(request, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_year(request, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions


#_________________________________________________________________________________________________________________________

def all_spendings_in_past_week_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_week_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_month_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_month_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_year_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_year_by_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

#_________________________________________________________________________________________________________________________
# by MODEL Concrete Category 
def all_spendings_for_model_category(request, category_name):
    model_category = ModelConcreteCategory.objects.filter(user=request.user).get(current_name=category_name)

    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category=model_category).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_week_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_week_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_week(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_month_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_month_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_month(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_past_year_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = past_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions

def all_spendings_in_this_year_by_model_category(request, category_name, start_date=None, end_date=None):
    start_date, end_date = this_year(start_date, end_date)
    transactions = []
    for each in Spending.objects.filter(user_id=request.user.id, category__model_concrete_category__current_name=category_name, date__range=(start_date, end_date)).values():
            category = ConcreteCategory.objects.filter(id=each.get("category_id")).first()
            newSpending = [each.get("title"), each.get("description"), each.get("amount"), category.model_concrete_category, each.get("photo"), each.get("date"), each.get("id")]
            transactions.append(newSpending)
    return transactions
