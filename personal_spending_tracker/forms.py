from django import forms
from django.contrib.auth.forms import PasswordChangeForm
# Later when including javascript css - from bootstrap_datepicker_plus import DatePickerInput
from .models import User, Spending, ConcreteCategory, ModelConcreteCategory
from .helper_functions.CC_MCC_objects_retrieval import *
from datetime import date

class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
         model = User

         fields = ['first_name', 'last_name', 'username','email']
         widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
         }
         

    newPassword = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    passwordConfirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        super().clean()
        newPassword = self.cleaned_data.get('newPassword')
        passwordConfirmation = self.cleaned_data.get('passwordConfirmation')
        if newPassword != passwordConfirmation:
            self.add_error('passwordConfirmation', 'password confirmation must match the password')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            email = self.cleaned_data.get('email'),
            password=self.cleaned_data.get('newPassword')
        )
        return user


class DateInput(forms.DateInput):
    input_type = 'date'
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'date_of_birth']
        widgets = {
          'username': forms.TextInput(attrs={'readonly':'readonly'}),
          'email': forms.TextInput(attrs={'readonly':'readonly'}),
          'bio': forms.Textarea,
          'date_of_birth': DateInput()
        }
        
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            age = datetime.now().date() - dob
            if age < timedelta(days=365*16):
                raise forms.ValidationError("You must be at least 16 years old.")
        return dob

# add spending forms
class SpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['user', 'title', 'description', 'amount', 'photo', 'category', 'frequency', 'date', 'next_due_date', 'is_regular']
        widgets = {
            'user': forms.HiddenInput(attrs={'hidden': True}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'frequency' : forms.Select(attrs={'class': 'form-control'}),
            'date' : DateInput(attrs={'class': 'form-control'}),
            'next_due_date' : DateInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_regular': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user' : '',
            'title' : 'Title',
            'description': 'Description',
            'amount' : 'Amount',
            'photo' : 'Photo',
            'frequency' : 'Frequency',
            'next_due_date' : 'Next_due_date',
            'category': 'Category',
            'is_regular': 'Is Regular'
        }
    

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput(attrs={'hidden': True})
        self.fields['category'].queryset = get_active_model_concrete_categories(user)
        self.fields['category'].required = True
        self.fields['frequency'].required = False
        self.fields['next_due_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_regular = cleaned_data.get('is_regular')
        frequency = cleaned_data.get('frequency')
        next_due_date = cleaned_data.get('next_due_date')
        date = cleaned_data.get('date')
        model_concrete_category = cleaned_data.get('category')

        if model_concrete_category:
            concrete_category = get_active_concrete_categories(model_concrete_category)
            cleaned_data['category'] = concrete_category
        if is_regular and (not frequency and not next_due_date):
            raise forms.ValidationError('The next due date and frequency must be assigned to the spending when is regular is checked.')
        if is_regular and not frequency:
            raise forms.ValidationError('The frequency must be assigned to the spending when is regular is checked.')
        if is_regular and not next_due_date:
            raise forms.ValidationError('The next due date must be assigned to the spending when is regular is checked.')
        if not is_regular and next_due_date:
            raise forms.ValidationError('The next due date or frequency cannot be assigned to the spending when is regular is unchecked.')
        if next_due_date and next_due_date < date:
            raise forms.ValidationError('The next due date assigned to the spending cannot be less than the current spending date, i.e. ' + date.strftime('%d-%m-%Y'))
        
        return cleaned_data

        
class EditSpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['title', 'description', 'amount', 'photo', 'category','frequency', 'date', 'next_due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'date' : DateInput(attrs={'class': 'form-control'}),
            'frequency' : forms.Select(attrs={'class': 'form-control'}),
            'next_due_date' : DateInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_regular': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'amount' : 'Amount',
            'photo' : 'Photo',
            'date' : 'Date',
            'frequency' : 'Frequency',
            'next_due_date' : 'Next_due_date',
            'category': 'Category'
        }


    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(category, category) for category in categories]
        self.fields['frequency'].required = False
        self.fields['next_due_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_regular = cleaned_data.get('is_regular')
        frequency = cleaned_data.get('frequency')
        next_due_date = cleaned_data.get('next_due_date')

        if is_regular and (not frequency or not next_due_date):
            raise forms.ValidationError("frequency and next due date fields cannot be empty for regular spendings.")
        
# This a form to Change Password
class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "The new password fields didn't match.")

        return cleaned_data
    
    def clean_new_password1(self):
        return self.cleaned_data['new_password1']

    def clean_new_password2(self):
        return self.cleaned_data['new_password2']
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Invalid old password')
        return old_password

# category management forms 
class AddConcreteCategory(forms.ModelForm):
    class Meta:
        model = ConcreteCategory
        fields = ['name', 'limit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'limit': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddConcreteCategoryAccountsSession(forms.ModelForm):
    class Meta:
        model = ConcreteCategory
        fields = ['model_concrete_category', 'limit', 'goal_as_little_as_possible', 'goal_well_distributed', 'goal_x_less']
        widgets = {
            'limit': forms.TextInput(attrs={'class': 'form-control'}),
            'model_concrete_category': forms.Select(attrs={'class': 'form-control'}),
            'goal_x_less' : forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_concrete_category'].queryset = get_model_concrete_categories(user)
        self.user = user 

    def clean(self):
        # create a new cycle
        print('clean function entered')
        most_recent_cycle = get_the_most_recent_cycle(self.user)
        start_date = get_first_expiration_date_for_cycle(most_recent_cycle)
        today_date = date.today()
        new_cycle = Cycle.objects.create(user=self.user, start_date=start_date, cycle_length=self.user.cycle_length, accounts_session_date=today_date)
        print('a cycle chould have been created')
        cleaned_data = super().clean()
        cleaned_data['user'] = self.user
        cleaned_data['name'] = self.model_concrete_category.current_name
        cleaned_data['cycle'] = new_cycle
        return cleaned_data


class AddModelConcreteCategory(forms.ModelForm):
    class Meta:
        model = ModelConcreteCategory
        fields = ['current_name']
        widgets = {
            'current_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RenameConcreteCategory(forms.ModelForm):
    class Meta:
        model = ConcreteCategory
        fields = ['name']
        


