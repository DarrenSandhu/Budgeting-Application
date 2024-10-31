from ..models import ConcreteCategory, ModelConcreteCategory
from .cycle_objects_retrieval_and_modification import *

def get_model_concrete_categories(user):
    return ModelConcreteCategory.objects.filter(user=user)

def get_active_concrete_categories(model_concrete_category):
    user = model_concrete_category.user
    current_cycle = get_active_cycle_for_user_HS(user)
    concrete_categories=ConcreteCategory.objects.filter(
        user=user, 
        cycle=current_cycle,
        model_concrete_category=model_concrete_category
        )
    for concrete_category in concrete_categories:
        if concrete_category:
            return concrete_category
    return None

def get_active_model_concrete_categories(user):
    current_cycle = get_the_active_cycle_for_user(user)
    concrete_categories = ConcreteCategory.objects.filter(user=user, cycle=current_cycle)
    model_concrete_categories = ModelConcreteCategory.objects.filter(category__in=concrete_categories).values('id').distinct()
    return ModelConcreteCategory.objects.filter(id__in=model_concrete_categories)

def get_active_and_inactive_MCCs(user):
    current_cycle = get_the_active_cycle_for_user(user)
    active_concrete_categories = ConcreteCategory.objects.filter(user=user).filter(cycle=current_cycle)

    active_model_concrete_categories_ids = active_concrete_categories.values_list('model_concrete_category', flat=True)
    active_model_concrete_categories = ModelConcreteCategory.objects.filter(id__in=active_model_concrete_categories_ids)
    inactive_model_concrete_categories = ModelConcreteCategory.objects.filter(user=user).exclude(id__in=active_model_concrete_categories_ids)
    return active_model_concrete_categories, inactive_model_concrete_categories

