from django.contrib import admin

from .models import User, TemplateCategory, ConcreteCategory, Spending, ModelConcreteCategory, Cycle, PointReward

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'cycle_length')
        
@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'limit')

@admin.register(ConcreteCategory)
class ConcreteCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'limit', 'cycle', 'model_concrete_category', 'goal_as_little_as_possible', 'goal_well_distributed', 'goal_x_less')
        
@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'date', 'amount', 'description', 'category')

@admin.register(ModelConcreteCategory)
class ModelConcreteCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_name')

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'cycle_length', 'accounts_session_date')

@admin.register(PointReward)
class PointRewardAdmin(admin.ModelAdmin):
    list_display = ('cycle', 'points', 'rewarding_for', 'category')

    