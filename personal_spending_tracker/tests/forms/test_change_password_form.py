from datetime import date
from django.test import TestCase
from personal_spending_tracker.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from personal_spending_tracker.forms import PasswordForm

class PasswordFormTestCase(TestCase):
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
        self.user.set_password('oldpassword')
        # self.user.save()
        self.form_data = {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }

    def test_form_valid(self):
        form = PasswordForm(data=self.form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_new_passwords_not_matching(self):
        self.form_data['new_password2'] = 'differentpassword'
        form = PasswordForm(data=self.form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)

    def test_form_invalid_old_password_not_valid(self):
        self.form_data['old_password'] = 'wrongpassword'
        form = PasswordForm(data=self.form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
    