from django.test import TestCase
from django.contrib.auth.models import User
from personal_spending_tracker.forms import EditUserForm, DateInput
from datetime import date, timedelta, datetime
from django.contrib.auth import get_user_model
from django import forms



class EditUserFormTestCase(TestCase):

    def setUp(self):
        UserModel = get_user_model()
        self.user = UserModel.objects.create(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            bio='This is a test user',
            date_of_birth=date(2000, 1, 1),
            cycle_length='MONTHLY'
        )
        self.form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'This is an updated bio',
            'date_of_birth': date(1990, 1, 1)
        }

    def test_valid_form(self):
        form = EditUserForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_empty_fields(self):
        form_data = {
            'username': '',
            'email': '',
            'bio': '',
            'date_of_birth': ''
        }
        form = EditUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_username_length(self):
        form_data = self.form_data.copy()
        form_data['username'] = 'abc'
        form = EditUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_valid_date_of_birth(self):
        form_data = self.form_data.copy()
        form_data['date_of_birth'] = date.today() - timedelta(days=365*20)
        form = EditUserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_date_of_birth(self):
        form_data = self.form_data.copy()
        form_data['date_of_birth'] = date.today() - timedelta(days=365*15)  # younger than 16 years old
        form = EditUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['date_of_birth'], ['You must be at least 16 years old.'])
    
    def test_email_field_readonly(self):
        form = EditUserForm(instance=self.user)
        email_field = form.fields.get('email')
        self.assertTrue(email_field.widget.attrs.get('readonly'))

    def test_username_field_readonly(self):
        form = EditUserForm(instance=self.user)
        username_field = form.fields.get('username')
        self.assertTrue(username_field.widget.attrs.get('readonly'))

    def test_bio_field_type(self):
        form = EditUserForm(instance=self.user)
        bio_field = form.fields.get('bio')
        self.assertIsInstance(bio_field.widget, forms.Textarea)

    def test_date_of_birth_field_type(self):
        form = EditUserForm(instance=self.user)
        dob_field = form.fields.get('date_of_birth')
        self.assertIsInstance(dob_field.widget, DateInput)

    def test_date_of_birth_validation_error_message(self):
        form_data = self.form_data.copy()
        form_data['date_of_birth'] = date.today() - timedelta(days=365*15)  # younger than 16 years old
        form = EditUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        expected_error = ['You must be at least 16 years old.']
        self.assertEqual(form.errors['date_of_birth'], expected_error)

    def test_date_of_birth_validation_no_error_message(self):
        form_data = self.form_data.copy()
        form_data['date_of_birth'] = date.today() - timedelta(days=365*20)  # older than 16 years old
        form = EditUserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertNotIn('date_of_birth', form.errors)