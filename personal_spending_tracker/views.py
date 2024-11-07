from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse
from personal_spending_tracker.helper_functions.filter_points import *
from django.contrib.auth import update_session_auth_hash


from personal_spending_tracker.helper_functions.upcoming_spending import *
from .forms import EditSpendingForm, LogInForm, SignUpForm, EditUserForm, PasswordForm, SpendingForm, AddConcreteCategory, AddConcreteCategoryAccountsSession, RenameConcreteCategory, AddModelConcreteCategory
from .models import Spending, TemplateCategory, ConcreteCategory, Cycle
from .utils import create_concrete_default_categories
from django.db import IntegrityError
from .management.commands.seed_functions import seed_template_categories
import json
from .helper_functions.json_processing import DecimalEncoder
from personal_spending_tracker.helper_functions.filter_all_spending import *

from .helper_functions.view_access_restrictors import ViewFilter
from .helper_functions.filter_spendingAmount_by_category_date import *
from .helper_functions.chart_context_genaration import *
from .helper_functions.spending_history_data import *
from .helper_functions.spending_history_data_objects import *

from .helper_functions.cycle_dates_computation import *
from .helper_functions.cycle_objects_retrieval_and_modification import *
from .views_achievements_points import category_savings
from .helper_functions.CC_MCC_objects_retrieval import *


import datetime 
import calendar

from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

import math

from django.forms import formset_factory, modelformset_factory
from django.views.generic import TemplateView

@ViewFilter.prohibit_anonymous
def feed(request):
    # CURRENT BUDGET STATE DATA
    timeframe_string_now = ""
    current_cycle = get_the_active_cycle_for_user(request.user)
    if current_cycle: 
        # get the timeframe string of the cycle  
        timeframe_string_now = current_cycle.start_date.strftime('%d-%m-%Y') + " to " + get_last_cycle_date(current_cycle).strftime('%d-%m-%Y')

    current_active_cycle = get_active_cycle_for_user_HS(user = request.user)
    if current_active_cycle:
        if get_first_expiration_date_for_cycle_HS(current_active_cycle) == date.today():
            messages.info(request, mark_safe("Your accounts session for your recent cycle is now available. Click here to review it: <a href=/accounts_session_1_add_additional_spendings_for_recent_cycle/Cycle/All/Current>Accounts Session</a>"))


    today = json.dumps(date.today().day)
    month_2 = date.today().strftime('%B')  # Get the full month name

    context = {
        'timeframe_string_now' : timeframe_string_now, 
        'today' : today,
        'month_2' : month_2,
    }
    context.update(fetch_context_cycle_budget_current_state_chart_o_category(current_active_cycle))

    return render(request, 'feed.html', context)

@ViewFilter.prohibit_anonymous
def cycle_finance_report(request):
    # PREVIOUS CYCLE REPORT DATA 
    timeframe_string_report = ""
    previous_cycle_json_string_data_context = {}

    previous_cycle = get_previous_active_cycle_for_user(request.user)
    if previous_cycle:
        # get the timeframe string of the cycle  
        timeframe_string_report = previous_cycle.start_date.strftime('%d-%m-%Y') + " to " + get_last_cycle_date(previous_cycle).strftime('%d-%m-%Y')
        previous_cycle_json_string_data_context.update(fetch_context_past_cycle_report_chart_o_category(previous_cycle))

    today = json.dumps(date.today().day)

    context = {
        'timeframe_string_report' : timeframe_string_report,
        'today' : today,
    }
    context.update(previous_cycle_json_string_data_context)

    return render(request, 'cycle_finance_report.html', context)

def test(request):
    return render(request, 'layout_test.html')

def home(request):
    if request.user.is_authenticated:
                return redirect('feed')
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if form.is_valid():
            # USER CREATED
            user = form.save()

            #
            #seed_template_categories()
            # TEMPATE CATEGORIES CREATED FOR A USER
            create_concrete_default_categories(user)
            # CYCLE FOR A USER CREATED
            # ensure there exists an active cycle 
            ensure_an_active_cycle(user)
            #

            #Welcome Email
            mydict = {'first_name': first_name, 'last_name' : last_name}
            html_template = 'welcome_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome To Personal Spending Tracker'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,email_from, recipient_list)
            message.content_subtype = 'html'
            #message.send()
            #Welcome Email
            
            login(request, user)
            messages.success(request, "Signed up successfully")
            return redirect('feed')
        # else:
        #     messages.add_message(request,messages.ERROR, "Invalid Input")
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form':form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(data = request.POST)
        username = request.POST['username']
        if form.is_valid():
            seed_template_categories()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                # CYCLE FOR A USER CREATED
                # ensure there exists an active cycle
                if user.username != 'user_account_session1' and user.username !='user_account_session2':
                    ensure_an_active_cycle(user)
            return redirect('feed')
    messages.add_message(request,messages.ERROR, "Invalid credentials")
    form = LogInForm()
    return render(request, 'log_in.html', {'form':form, 'request' : request})

@ViewFilter.prohibit_anonymous
def spending_by_category(request):
    # split into active and inactive 
    active_model_concrete_categories, inactive_model_concrete_categories = get_active_and_inactive_MCCs(request.user)

    active_category_filters = active_model_concrete_categories.values_list('current_name', flat=True)
    no_of_active_categories = len(active_category_filters)
    inactive_category_filters = inactive_model_concrete_categories.values_list('current_name', flat=True)
    no_of_inactive_categories = len(inactive_category_filters)

    context = {
        'no_of_active_categories' : no_of_active_categories,
        'no_of_inactive_categories' : no_of_inactive_categories,
        'active_category_filters' : active_category_filters, 
        'inactive_category_filters' : inactive_category_filters,
    }
    return render(request, 'spending_by_category.html', context)

@ViewFilter.prohibit_anonymous
def spending_by_inactive_model_category(request, categoryfilter):
    # get the relevant category 
    model_category = ModelConcreteCategory.objects.filter(user=request.user).get(current_name=categoryfilter)
    category_name = model_category.current_name
    # get all the cycles for that model category 
    cycles_ids = ConcreteCategory.objects.filter(model_concrete_category=model_category).values_list('cycle', flat=True)
    cycles = Cycle.objects.filter(id__in=cycles_ids)

    timeframe_strings = []
    cycles_ids = []
    for cycle in cycles:
        timeframe_strings.append(cycle.start_date.strftime('%d-%m-%Y') + " to " + get_last_cycle_date(cycle).strftime('%d-%m-%Y'))
        cycles_ids.append(cycle.id)

    no_of_cycles = len(cycles)

    cycles_timeframes_ids = zip(timeframe_strings, cycles_ids)

    context = {
        'cycles_timeframes_ids' : cycles_timeframes_ids,
        'no_of_cycles' : no_of_cycles,
        'category_name' : category_name,
    }
    return render(request,'spending_by_inactive_model_category.html', context)

#tests:
# does the json contain the same amount of spending objects cumulatively as initailly retrieved from the database?
@ViewFilter.prohibit_anonymous
def spending_by_category_concrete_category(request, timefilter, categoryfilter, cyclefilter):
    # get the relevant category 
    model_category = ModelConcreteCategory.objects.filter(user=request.user).get(current_name=categoryfilter)
    context_second_chart = {}
    if cyclefilter=="Current":
        # i.e. default, current cycle requested 
        cycle = get_the_active_cycle_for_user(request.user)
        category = ConcreteCategory.objects.filter(user=request.user).filter(cycle=cycle).get(model_concrete_category=model_category)
        today = json.dumps(date.today().day)
        # 2. outsource single category cumulative bar chart context fetching
        context_second_chart = {
            'today' : today,
        }
        context_second_chart.update(fetch_context_cycle_budget_current_state_chart_o_category(cycle, category))
    else: 
        # i.e. a specific cycle from the past requested 
        cycle = Cycle.objects.get(id=cyclefilter)
        category = ConcreteCategory.objects.filter(user=request.user).filter(cycle=cycle).get(model_concrete_category=model_category)
        # as it's irrelevant to a past cycle - a flag that will deactivate "now" markers on charts 
        today = '0'
        # 2. outsource single category cycle report bar chart context fetching
        timeframe_string = cycle.start_date.strftime('%d-%m-%Y') + " to " + get_last_cycle_date(cycle).strftime('%d-%m-%Y')
        context_second_chart = {
            'timeframe_string' : timeframe_string,
            'today' : today,
        }
        context_second_chart.update(fetch_context_past_cycle_report_chart_o_category(cycle, category))
        
    
    # 1. outsource distribution chart context fetching 
    context_distribution_chart = fetch_context_for_distribution_chart(request, category, cycle)

    # 3. outsource history context fetching 
    context_history = fetch_context_for_spending_history_data_objects(request, timefilter, categoryfilter, cyclefilter)

    number_of_days = get_number_of_days_for_cycle(cycle)

    context = {
        'category' : category, 
        'number_of_days' : number_of_days,
    } 
    context.update(context_distribution_chart)
    context.update(context_second_chart)
    context.update(context_history)

    return render(request, 'spending_by_category_concrete_category.html', context)

@ViewFilter.prohibit_anonymous
def log_out(request):
    logout(request)
    return redirect('home')

@ViewFilter.prohibit_anonymous
# @login_required
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = EditUserForm(data = request.POST, instance = current_user)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('home')
    else:
        form = EditUserForm(instance = current_user)
    return render(request, 'edit_profile.html', {'form': form, 'request' : request})

@ViewFilter.prohibit_anonymous
def change_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(current_user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, current_user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
    else:
        form = PasswordForm(current_user)
    return render(request, 'change_password.html', {'form': form, 'request' : request})

@ViewFilter.prohibit_anonymous
def add_spending(request):
    if request.method == 'POST':
        form = SpendingForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            if not instance.is_regular:
                instance.frequency = None
                instance.next_due_date = None
            
            if 'photo' in request.FILES:
                instance.photo = request.FILES['photo']
                
            instance.save()
            remaining = category_savings(request.user, instance.category_id)
            if remaining <=0:
                    messages.error(request, 'You have Exceeded the budget limit !!.')
            elif remaining<10:
                   messages.warning(request, 'You have Exceeded 90%" of the BUdget!.')
            
            # redirect('spending_history', kwargs={'timefilter': 'All', 'categoryfilter': 'All', 'cyclefilter' : 'Current'})
            return HttpResponseRedirect(reverse('spending_history', kwargs={'timefilter': 'All', 'categoryfilter': 'All', 'cyclefilter' : 'Current'}))
    else:
        form = SpendingForm(request.user)
    return render(request, 'add_spending.html', {'form': form, 'request' : request})


def spending_history(request, timefilter, categoryfilter, cyclefilter):
    context = fetch_context_for_spending_history_data_objects(request, timefilter, categoryfilter, cyclefilter)
    return render(request, 'spending_history.html', context)

from uuid import UUID
def edit_spending(request, spending_id):
    spending = get_object_or_404(Spending, id=UUID(spending_id))
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if 'frequency' in request.POST:
            frequency = request.POST.get('frequency')
        else:
            frequency = None
        
        if 'is_regular' in request.POST:
            is_regular = request.POST.get('is_regular')
        else:
            is_regular = False

        if 'next_due_date' in request.POST:
            next_due_date = request.POST.get('next_due_date')
        else:
            next_due_date = None

        model_concrete_category_name = request.POST.get('category')
        model_concrete_category = ModelConcreteCategory.objects.get(current_name=model_concrete_category_name)
        print(model_concrete_category_name)
        concrete_category = get_active_concrete_categories(model_concrete_category)
        

        photo = request.FILES.get('photo')

        date = request.POST.get('date')
        
        if not is_regular:
            frequency = None
            next_due_date = None
        

        # Update the spending object
        spending.title = title
        spending.description = description
        spending.amount = amount
        spending.category = concrete_category
        spending.photo = photo
        spending.date = date
        spending.frequency = frequency
        spending.is_regular = is_regular
        spending.next_due_date = next_due_date
        spending.save()
        
        return HttpResponseRedirect(reverse('spending_history', kwargs={'timefilter': 'All', 'categoryfilter': 'All', 'cyclefilter' : 'Current'}))
    else:
        context = {'spending': spending, 'timefilter': 'All', 'categoryfilter': 'All', 'cyclefilter' : 'Current'}
        return render(request, 'spending_history.html', context)
    
import datetime
def regular_spendings_chart(request):
    all_regular_spendings = get_all_regular_spendings(request)
    all_close_spendings = get_all_close_regular_spendings(request)
    all_far_spendings = get_all_far_regular_spendings(request)

    chart_data = []
    for spending in all_regular_spendings:
        today = spending.date
        days_remaining = (spending.next_due_date - today).days
        chart_data.append({
            'title': spending.title,
            'amount': spending.amount,
            'days_remaining': days_remaining,
            'is_close': spending in all_close_spendings,
        })
    
    context = {
        'chart_data': chart_data,
    }
    if not all_regular_spendings:
        context['no_regular_spendings'] = True

    return render(request, 'regular_spendings_chart.html', context)

def delete_spending(request, spending_id):
    # Get the spending object with the specified id, or return a 404 error page
    spending = get_object_or_404(Spending, id=UUID(spending_id))
    
    # Delete the spending object
    spending.delete()
    
    # Redirect to the spending history page with default filters
    return HttpResponseRedirect(reverse('spending_history', kwargs={'timefilter': 'All', 'categoryfilter': 'All', 'cyclefilter' : 'Current'}))

def accounts_session_1_add_additional_spendings_for_recent_cycle(request, timefilter, categoryfilter, cyclefilter):
    active_cycle = get_active_cycle_for_user_HS(user = request.user)
    context_history = fetch_context_for_spending_history_data_objects(request, timefilter, categoryfilter, cyclefilter)
    context = {
        'start_date' : active_cycle.start_date,
        'end_date' : get_first_expiration_date_for_cycle_HS(active_cycle)
    }
    context.update(context_history)
    return render(request, 'accounts_session_1_add_additional_spendings_for_recent_cycle.html', context)

def accounts_session_3_points_summary(request):
    current_user = request.user
    achievements = []
    categories = []
    no_of_achievements = 0

    # Retrieve all categories for user for filter dropdown
    for cat in ModelConcreteCategory.objects.filter(user_id=current_user.id).values():
        categories.append(cat.get("current_name"))
    categories.append("Cycle-Specific")
    
    # Retrieve reward_title, points,  category, and session_date for each achievememt for the user
    achievements = all_points_for_active_cycle(request)
    
    no_of_achievements = len(achievements)
    
    return render(request, 'accounts_session_3_points_summary.html', {'categories':categories, 'no_of_achievements':no_of_achievements, 'achievements':achievements})

def accounts_session(request):
    current_active_cycle = get_active_cycle_for_user_HS(request.user)
    categories = ConcreteCategory.objects.filter(user = request.user).filter(cycle = current_active_cycle)
    edit_cat = False
    edit_lim = False
    category = None
    template_categories = ModelConcreteCategory.objects.filter(user = request.user)
    for each in template_categories:
        if each.current_name in categories:
            template_categories.delete(each)
    add_cat = False 

    if request.method == 'POST':
        if 'delete' in request.POST:
            try: 
                category = ConcreteCategory.objects.filter(user = request.user).get(name=request.POST.get('delete'))
                categories.delete(category)
                context = {
                    'request' : request, 
                    'categories' : categories,
                    'category_p' : category, 
                    'edit_cat' : edit_cat,
                    'edit_lim' : edit_lim, 
                    'add_cat' : add_cat
                }
                return render(request, 'accounts_session.html', context)
            except:
                redirect('accounts_session')

        elif 'rename' in request.POST:
            category = request.POST.get('rename')
            edit_cat = True 
            context = {
                'request' : request, 
                'categories' : categories,
                'category_p' : category, 
                'edit_cat' : edit_cat,
                'edit_lim' : edit_lim, 
                'add_cat' : add_cat
            }
            return render(request, 'accounts_session.html', context)
        
        elif 'rename_ok' in request.POST:
            #TODO: check for whether theres a categopry called like this for the user already
            try: 
                category = ConcreteCategory.objects.filter(user = request.user).get(id=request.POST.get('rename_ok'))
                category.name = request.POST.get('category_name', '')
                try: 
                    category.save()
                    redirect('accounts_session')
                except IntegrityError:
                        error = "A category with this name already exists!"
                        error_present = True 
                        context = {
                            'request' : request, 
                            'categories' : categories,
                            'category_p' : category, 
                            'edit_cat' : edit_cat,
                            'edit_lim' : edit_lim, 
                            'add_cat' : add_cat, 
                            'error' : error,
                            'error_present' : error_present 
                        }
                        return render(request, 'accounts_session.html', context)
            except:
                redirect('accounts_session')
        
        elif 'edit_limit' in request.POST:
            category = request.POST.get('edit_limit')
            edit_lim = True 
            context = {
                'request' : request, 
                'categories' : categories,
                'category_p' : category, 
                'edit_cat' : edit_cat,
                'edit_lim' : edit_lim, 
                'add_cat' : add_cat
            }
            return render(request, 'accounts_session.html', context)
        
        elif 'edit_limit_ok' in request.POST:
            try: 
                category = ConcreteCategory.objects.filter(user = request.user).get(id=request.POST.get('edit_limit_ok'))
                category.limit = request.POST.get('limit', '')
                category.save()
                redirect('accounts_session')
            except:
                redirect('accounts_session')

        elif 'add_category' in request.POST:
            print("add cat")
            add_cat = True 
            print("add cat 2")
            form = AddConcreteCategoryAccountsSession()
            print("add cat 3")
            # template_categories = TemplateCategory.objects.all()
            context = {
                'request' : request, 
                'categories' : categories,
                'category_p' : category, 
                'edit_cat' : edit_cat,
                'edit_lim' : edit_lim, 
                'add_cat' : add_cat, 
                'form' : form ,
                'template_categories': template_categories
            }
            return render(request, 'accounts_session.html', context)
        
        elif 'add_category_ok' in request.POST:
            form = AddConcreteCategoryAccountsSession(request.POST)
            if form.is_valid():
                try:
                    concrete_category = form.save(commit=False)
                    concrete_category.user = request.user
                    concrete_category.save()
                    redirect('accounts_session')
                except IntegrityError:
                    error = "A category with this name already exists!"
                    error_present = True 
                    context = {
                        'request' : request, 
                        'categories' : categories,
                        'category_p' : category, 
                        'edit_cat' : edit_cat,
                        'edit_lim' : edit_lim, 
                        'add_cat' : add_cat, 
                        'form' : form,
                        'error' : error,
                        'error_present' : error_present,
                        'template_categories': template_categories 
                    }
                    return render(request, 'accounts_session.html', context)
        elif 'confirm_accounts_session' in request.POST:
            try:
                current_active_cycle.accounts_session_date = date.today()
                current_active_cycle.save()
                new_active_cycle = Cycle.objects.create(
                    user = request.user,
                    start_date = current_active_cycle.start_date + timedelta(days=1),
                    cycle_length = current_active_cycle.cycle_length
                )
                goal_x_less_list = request.POST.getlist('goal_x_less')
                counter = 0
                for each in categories:
                    category = ConcreteCategory.objects.filter(user = request.user).get(id=each.id)
                    new_category = ConcreteCategory.objects.create(
                        name = category.name,
                        limit = category.limit,
                        user = request.user,
                        cycle = new_active_cycle,
                        model_concrete_category = category.model_concrete_category,
                        goal_as_little_as_possible = 0,
                        goal_well_distributed = 0,
                        goal_x_less = 0
                    )
                    if str(category.id) in request.POST.getlist('minimal_spending'):
                        new_category.goal_as_little_as_possible = 1
                    if str(category.id) in request.POST.getlist('well_distributed_spending'):
                        new_category.goal_well_distributed = 1
                    new_category.goal_x_less = goal_x_less_list[counter]
                    counter += 1
                    new_category.save()
                redirect('accounts_session')
            except:
                redirect('accounts_session')
                
    context = {
        'request' : request, 
        'categories' : categories,
        'category_p' : category, 
        'edit_cat' : edit_cat,
        'edit_lim' : edit_lim, 
        'add_cat' : add_cat,
        'template_categories': template_categories
    }
    return render(request, 'accounts_session.html', context)

def category_management_dashboard(request):

    active_model_concrete_categories, inactive_model_concrete_categories = get_active_and_inactive_MCCs(request.user)
    edit_cat = False
    category = None

    if request.method == 'POST':
        if 'rename' in request.POST:
            category = request.POST.get('category')
            edit_cat = True 
            context = {
                'request' : request, 
                'active_model_concrete_categories' : active_model_concrete_categories,
                'inactive_model_concrete_categories' : inactive_model_concrete_categories,
                'category_processed_string' : category, 
                'edit_cat' : edit_cat,
            }
            return render(request, 'category_management_dashboard.html', context)
        
        elif 'rename_ok' in request.POST:
            try: 
                category = ModelConcreteCategory.objects.filter(user = request.user).get(id=request.POST.get('category_id'))
                new_name =  request.POST.get('category_name')
                category.current_name = new_name
                category.save()
                # changing names of all the related concrete categories
                concrete_categories_linked = ConcreteCategory.objects.filter(model_concrete_category=category)
                for concrete_category in concrete_categories_linked:
                    concrete_category.name = new_name
                    concrete_category.save()
            except IntegrityError:
                error = "A category with this name already exists!"
                context = {
                    'request' : request, 
                    'active_model_concrete_categories' : active_model_concrete_categories,
                    'inactive_model_concrete_categories' : inactive_model_concrete_categories,
                    'category_processed_string' : category, 
                    'edit_cat' : edit_cat,
                    'error' : error,
                }
                return render(request, 'category_management_dashboard.html', context)
        
    context = {
        'request' : request, 
        'active_model_concrete_categories' : active_model_concrete_categories,
        'inactive_model_concrete_categories' : inactive_model_concrete_categories,
        'category_processed_string' : category, 
        'edit_cat' : edit_cat,
    }
    return render(request, 'category_management_dashboard.html', context)

"""def accounts_session_2(request):
    template = 'accounts_session_2.html'
    most_recent_cycle = get_the_most_recent_cycle(request.user)
    most_recent_cycle_categories = ConcreteCategory.objects.filter(cycle=most_recent_cycle)
    AccountsSessionFormSet = formset_factory(
        form=AddConcreteCategoryAccountsSession, can_delete=True, extra=1, max_num=20
    )
    add_new_MCC_form = AddModelConcreteCategory()

    if request.method == 'POST':
        formset = AccountsSessionFormSet(request.POST, initial=most_recent_cycle_categories.values(), form_kwargs={'user': request.user})
        add_new_MCC_form = AddModelConcreteCategory(request.POST)
        if formset.is_valid():
            formset.save()
    else: 
        formset = AccountsSessionFormSet(initial=most_recent_cycle_categories.values(), form_kwargs={'user': request.user})
        add_new_MCC_form = AddModelConcreteCategory()

    return render(request, template, {'formset': formset, 'form2' : add_new_MCC_form})
"""

def accounts_session_2(request):
    # load the page set up
    template = 'accounts_session_2.html'
    # initial data retrieval 
    most_recent_cycle = get_the_most_recent_cycle(request.user)
    most_recent_cycle_categories = ConcreteCategory.objects.filter(cycle=most_recent_cycle)

    # setting up a formset factory 
    AccountsSessionFormSet = formset_factory(
        form=AddConcreteCategoryAccountsSession, can_delete=True, extra=0, max_num=20
    )

    # creating forms:
    accounts_session_formset = AccountsSessionFormSet(request.POST or None, initial=most_recent_cycle_categories.values(), form_kwargs={'user': request.user})
    add_new_MCC_form = AddModelConcreteCategory(request.POST or None)

    if request.method == 'POST':
        if 'accounts_session_formset-submit' in request.POST:
            accounts_session_formset = AccountsSessionFormSet(request.POST)
            print(accounts_session_formset)
            print('accounts_session_formset submission detected')
            # create a new cycle 
            if accounts_session_formset.is_valid():
                #start_date = get_first_expiration_date_for_cycle(most_recent_cycle)
                #today_date = date.today()
                #new_cycle = Cycle.objects.create(user=request.user, start_date=start_date, cycle_length=request.user.cycle_length, accounts_session_date=today_date)
                print(accounts_session_formset)
                for form in accounts_session_formset:
                    print('entered for loop')
                    instance = form.save(commit=False)
                    try: 
                        #instance.name = instance.model_concrete_category.current_name
                        #instance.user = request.user 
                        #instance.cycle = new_cycle 
                        instance.save()
                        print('an instance should have been creaed')
                    except:
                        #new_cycle.delete()
                        print('a cycle chould have been deleted')
                        accounts_session_formset = AccountsSessionFormSet(initial=most_recent_cycle_categories.values(), form_kwargs={'user': request.user})
                        return render(request, template, {'formset': accounts_session_formset, 'form2' : add_new_MCC_form, 'error': "Something wrong with the form!"})
            else:
                print('error')
                # If the formset is invalid, print the errors associated with each form
                for form in accounts_session_formset:
                    print(form.errors)

         
        elif 'add_new_MCC_form-submit' in request.POST:
            if add_new_MCC_form.is_valid():
                # process data from form2
                model_concrete_category = add_new_MCC_form.save(commit=False)
                model_concrete_category.user = request.user
                try: 
                    model_concrete_category.save()
                except IntegrityError as e:
                    accounts_session_formset = AccountsSessionFormSet(initial=most_recent_cycle_categories.values(), form_kwargs={'user': request.user})
                    return render(request, template, {'formset': accounts_session_formset, 'form2' : add_new_MCC_form, 'error': "You already have a Model Category with this name!"})
                # set accounts_session_formset initial data - TODO: VERIFY IF WORKS
            if accounts_session_formset.is_valid():
                accounts_session_formset = AccountsSessionFormSet(initial=accounts_session_formset.cleaned_data, form_kwargs={'user': request.user})
            else: accounts_session_formset = AccountsSessionFormSet(initial=most_recent_cycle_categories.values(), form_kwargs={'user': request.user})

    return render(request, template, {'formset': accounts_session_formset, 'form2' : add_new_MCC_form})



# @ViewFilter.prohibit_anonymous
# def add_spending_category(request):
#     if request.method == 'POST':
#         form = AddConcreteCategory(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return redirect('category_management_dashboard')
#     else:
#         form = AddConcreteCategory()
#     return render(request, 'add_spending_category.html', {'form': form, 'request' : request})