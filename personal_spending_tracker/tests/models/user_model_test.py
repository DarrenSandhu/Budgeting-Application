from django.test import TestCase

# Create your tests here.

class UserModelTestCase(TestCase):
    #username cannot be longer than 30 characters
    #username cannot be blank
    #bio can be blank
    #bio cannot be over 500 characters