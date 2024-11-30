from ..models import ConcreteCategory, Spending
from .filter_all_spending import *
import math
import json
from .json_processing import *
from .cycle_objects_retrieval_and_modification import * 
from .cycle_dates_computation import *
from .spending_retrieval import *

def fetch_context_for_history_data(request, timefilter = "All", categoryfilter = "All", cyclefilter = "Current"):
    current_user = request.user
    transactions = []
    categories = []
    no_of_transactions = 0

    # Retrieve all categories for user for filter dropdown
    for cat in ModelConcreteCategory.objects.filter(user=current_user).values():
        categories.append(cat.get("current_name"))
    
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
        transactions = all_spendings_for_model_category(request, categoryfilter)
    else:
        if timefilter == "Past Week":
            transactions = all_spendings_in_past_week_by_model_category(request, categoryfilter)
        elif timefilter == "This Week":
            transactions = all_spendings_in_this_week_by_model_category(request, categoryfilter)
        elif timefilter == "Past Month":
            transactions = all_spendings_in_past_month_by_model_category(request, categoryfilter)
        elif timefilter == "This Month":
            transactions = all_spendings_in_this_month_by_model_category(request, categoryfilter)
        elif timefilter == "Past Year":
            transactions = all_spendings_in_past_year_by_model_category(request, categoryfilter)
        elif timefilter == "This Year":
            transactions = all_spendings_in_this_year_by_model_category(request, categoryfilter)
    
    no_of_transactions = len(transactions)

    spendings = Spending.objects.filter(user_id=current_user.id)

    context = { 
        'categoryfilter': categoryfilter, 
        'timefilter':timefilter, 
        'cyclefilter' : cyclefilter,
        'time_options': time_options, 
        'categories':categories, 
        'no_of_transactions':no_of_transactions, 
        'transactions':transactions,
        'spendings': spendings
        }

    return context

def fetch_context_for_distribution_chart(request, category, cycle):
    # spendings - relevant user, cycle, category
    all_spendings_this_cycle_this_category = get_cycle_spendings(request.user, cycle).filter(category=category)
    # sort the spending items into days of the cycle
    number_of_days = get_number_of_days_for_cycle(cycle)
    days = [i for i in range(1, number_of_days+1)]
    spendings_by_day = [[] for _ in range(number_of_days)]
    for spending in all_spendings_this_cycle_this_category:
        n = check_if_is_this_days_spending(spending, 0)
        spendings_by_day[n].append(spending)

    # "day" : {"spending", "spending", ...}
    graph_data = {}
    for day, spendings in zip(days, spendings_by_day):
        graph_data[day] = {"spendings" : spendings}
    # sort Spending objects into datasets so it is possible to display them as accumulated for each day on a bar chart 
    # max number of spendings within a day
    max_num_spendings = max(len(spending["spendings"]) for spending in graph_data.values())
    # Initialize a NumPy array to hold the data
    # data = np.zeros((len(graph_data), max_num_spendings))  # NumPy array (to be replaced)
    data = [[0] * max_num_spendings for _ in range(len(graph_data))]  # List of lists replacement

    # Fill the data array with spendings values
    for i, day in enumerate(graph_data.keys()):
        for j, spending in enumerate(graph_data[day]["spendings"]):
            data[i][j] = spending.amount
    
    # Convert the data to a list of dictionaries, one per the serial number of the day's spending 
    datasets = []
    for i in range(max_num_spendings):
        datasets.append({
            "label": f"Spending category {i}",
            "data": [day[i] for day in data]
        })

    cycle_distribution_of_spending_json_format_string = json.dumps(datasets, cls=DecimalEncoder, ensure_ascii=False)

    # average recommended thershold
    average_thershold = math.floor(category.limit/number_of_days)
    # average recommended thershold + 10% 
    average_thershold_devation_allowed = math.floor(average_thershold + average_thershold/10)

    context = {
        'distribution_chart_data' : cycle_distribution_of_spending_json_format_string,
        'average_thershold' : average_thershold,
        'average_thershold_devation_allowed' : average_thershold_devation_allowed,
    }
    
    return context

# return: a JSON format string that is suitable to be passed to Javascript script and used for chart generation 
def fetch_context_past_cycle_report_chart_o_category(cycle, category = None):
    if (category): 
        # for some specific category 
        categories = ConcreteCategory.objects.filter(id=category.id)
    else: 
        # for all categories for the cycle 
        categories = ConcreteCategory.objects.filter(user=cycle.user,cycle=cycle)
    
    categories_names = list(map(lambda category: category.model_concrete_category.current_name, categories))

    # budget data
    # TODO: what if budegt has changed already? We need some sort of model that will store HISTORIC ConcreteCategory data 
    budgets = list(map(lambda category: category.limit, categories))

    # spending data 
    sub_spendings = list()
    for this_category in categories: 
        category_spending = Spending.objects.filter(user=cycle.user).filter(category=this_category)
        category_spending_amounts =  list(map(lambda spending: spending.amount, category_spending))
        category_spending_amounts_summed = sum(category_spending_amounts, 0)
        sub_spendings.append(category_spending_amounts_summed)

    # formatting data in a form appropriate for passing to the html template
    data_report = {}
    for name, budget, spending in zip(categories_names, budgets, sub_spendings):
        data_report[name] = {"budget" : budget, "spending": spending}
    json_data_report = json.dumps(data_report, cls=DecimalEncoder, ensure_ascii=False)

    if len(sub_spendings) != 0:
        total_spending = sum(sub_spendings)
    else: 
        total_spending = 0

    context = {
       'json_data' : json_data_report,
       'total_spending' : total_spending,
    }

    return context

# return: a JSON format string that is suitable to be passed to Javascript script and used for chart generation
def fetch_context_cycle_budget_current_state_chart_o_category(cycle, category = None):
    if (category): 
        # for some specific category 
        categories = ConcreteCategory.objects.filter(id=category.id)
    else: 
        # for all categories for the cycle
        categories = ConcreteCategory.objects.filter(user=cycle.user).filter(cycle=cycle)

    categories_names = list(map(lambda category: category.model_concrete_category.current_name, categories))

    # spending and budget data
    sub_budget_left_percentage = list()
    sub_budget_left = list()
    number_of_days = get_number_of_days_for_cycle(cycle)
    for this_category in categories: 
        category_spending = Spending.objects.filter(user=cycle.user).filter(category=this_category)
        category_spending_amounts = list(map(lambda spending: spending.amount, category_spending))

        category_budget_left = this_category.limit - sum(category_spending_amounts, 0)
        sub_budget_left.append(category_budget_left)

        category_budget_left_percentage = (category_budget_left/this_category.limit)*number_of_days
        sub_budget_left_percentage.append(category_budget_left_percentage)

    # formatting data in a form appropraite for passing to the html template
    budgets = [number_of_days] * categories.count()
    data_now = {}
    for name, budget, percentage, money_left in zip(categories_names, budgets, sub_budget_left_percentage, sub_budget_left):
        data_now[name] = {"budget" : budget, "spending": percentage, "money_left": money_left}
    json_data_now = json.dumps(data_now, cls=DecimalEncoder, ensure_ascii=False)

    context = {
        'json_data' : json_data_now,
    }

    return context


