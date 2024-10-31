"""Log out view test"""
from django.test import TestCase
from django.urls import reverse
from personal_spending_tracker.forms import LogInForm
from personal_spending_tracker.models import User
from personal_spending_tracker.tests.helpers import *


class LogOutViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('log_out')
        User.objects.create_user('johndoe',
        email = 'johndoe@example.com',
        password = 'Password123')

    #correct url ?
    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')
        
    def test_get_log_out(self):
        self.client.login (username= 'johndoe', password= 'Password123') 
        self. assertTrue(self._user_is_logged_in()) 
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects (response, response_url, status_code=302, target_status_code=200) 
        self.assertTemplateUsed (response, 'home.html')
        self.assertFalse(self._user_is_logged_in())
        