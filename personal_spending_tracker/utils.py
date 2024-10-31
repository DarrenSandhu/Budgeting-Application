from .models import TemplateCategory, ModelConcreteCategory

# a function for creating user specific ccategories based on the templates provided by app creators 
def create_concrete_default_categories(user):
    
    template_categories = [
    {'name': 'Groceries', 'limit': 50.00},
    {'name': 'Gas', 'limit': 100.00},
    {'name': 'Movies', 'limit': 25.00},
    {'name': 'Rent', 'limit': 1000.00},
    {'name': 'Electricity', 'limit': 150.00}
]
    template_categories = TemplateCategory.objects.all()

    for category in template_categories: 
        ModelConcreteCategory.objects.create(current_name=category.name, user=user)
