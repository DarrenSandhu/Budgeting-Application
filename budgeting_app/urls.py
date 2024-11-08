"""budgeting_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from personal_spending_tracker import views, views_achievements_points
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_spending/', views.add_spending, name='add_spending'),
    path('spending_history/<str:timefilter>/<str:categoryfilter>/<str:cyclefilter>', views.spending_history, name='spending_history'),
    path('point_history/<str:timefilter>/<str:categoryfilter>/', views_achievements_points.point_history, name='point_history'),
    path('accounts_session_1_add_additional_spendings_for_recent_cycle/<str:timefilter>/<str:categoryfilter>/<str:cyclefilter>', views.accounts_session_1_add_additional_spendings_for_recent_cycle, name='accounts_session_1_add_additional_spendings_for_recent_cycle'),
    path('accounts_session_3_points_summary/', views.accounts_session_3_points_summary, name='accounts_session_3_points_summary'),
    path('accounts_session/', views.accounts_session_2, name='accounts_session'),
    path('edit_spending/<str:spending_id>/', views.edit_spending, name='edit_spending'),
    path('delete_spending/<str:spending_id>/', views.delete_spending, name='delete_spending'),


    #path('spending_history/<filter>', views.spending_history, name='spending_history'),
    # from my branch
    path('spending_by_category/', views.spending_by_category , name='spending_by_category'),
    path('spending_by_inactive_model_category/<str:categoryfilter>/', views.spending_by_inactive_model_category , name='spending_by_inactive_model_category'),
    path('spending_by_category/<str:timefilter>/<str:categoryfilter>/<str:cyclefilter>', views.spending_by_category_concrete_category , name='spending_by_category_concrete_category'),

    path('manage_categories_dashboard/', views.category_management_dashboard, name='category_management_dashboard'),
    
    path('test/', views.test, name='main'),

    path('cycle_finance_report/', views.cycle_finance_report, name='cycle_finance_report'),

    path('regular-spendings-chart/', views.regular_spendings_chart, name='regular_spendings_chart'),

    # path('add_category/', views.add_spending_category, name='add_category'),


]
# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

