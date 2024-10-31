"""Unit test cases for sign up form"""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from personal_spending_tracker.forms import SignUpForm
from personal_spending_tracker.models import User

class SignUpFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'newPassword': 'password123',
            'passwordConfirmation': 'password123',
        }

    def test_form_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        beforeCount = User.objects.count()
        form.save()
        afterCount = User.objects.count()
        self.assertEqual(afterCount, beforeCount+1)
        user = User.objects.get(username='johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')
        isPasswordCorrect = check_password('password123', user.password)
        self.assertTrue(isPasswordCorrect)

    def test_form_valid(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')

    def test_form_invalid_no_first_name(self):
        form_data = self.form_input.copy()
        form_data['first_name'] = ''
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())

    def test_form_invalid_no_last_name(self):
        form_data = self.form_input.copy()
        form_data['last_name'] = ''
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
    
    def test_form_invalid_no_username(self):
        form_data = self.form_input.copy()
        form_data['username'] = ''
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())
    
    def test_form_invalid_no_email(self):
        form_data = self.form_input.copy()
        form_data['email'] = ''
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
    
    def test_form_invalid_password_not_match_password_confirmation(self):
        self.form_input['passwordConfirmation'] = 'Pass1223'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('passwordConfirmation', form.errors.keys())
    
    def test_form_invalid_username_less_than_5_characters(self):
        self.form_input['username'] = 'bye'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())
    
    def test_form_invalid_email_format(self):
        self.form_input['email'] = 'bye'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

#password and username requirements, form uses model validation




    #password has correct format? , password and password confirmation are identicla
