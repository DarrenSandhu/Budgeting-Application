"""test log in form"""
from django import forms
from django.test import TestCase
from personal_spending_tracker.forms import LogInForm

class LogInFormTestCase(TestCase):

    def SetUp(self):
        self.form_input = {'username':'janedoe', 'password' : 'Password123'}

    #form contains required fields
    def test_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(password_field.widget, forms.PasswordInput)
    #form accepts valid input
    def test_form_accepts_valid_input(self):
        self.form_input = {'username':'janedoe', 'password' : 'Password123'}
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    #rejects blank username
    def test_reject_blank_username(self):
        self.form_input = {'username':'janedoe', 'password' : 'Password123'}
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    #rejects blank password
    def test_reject_blank_password(self):
        self.form_input = {'username':'janedoe', 'password' : 'Password123'}
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    #form accepts incorrect username
    def test_accepts_incorrect_username(self):
        self.form_input = {'username':'janedoe', 'password' : 'Password123'}
        self.form_input['username'] = 'ma'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    #form accepts incorrect password
    def test_accepts_incorrect_password(self):
        self.form_input = {'username':'janedoe', 'password' : 'Password123'}
        self.form_input['password'] = '123'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    #authenticate correctly valid user
    #invalid credentials do not authenticate
