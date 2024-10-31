" Tests for time frames views "
from django.test import TestCase
from datetime import datetime, timedelta
from calendar import monthrange
from personal_spending_tracker.tests.helpers import *
from personal_spending_tracker.models import Cycle, User
from personal_spending_tracker.helper_functions import views_time_frames



class TestTimeFramesViews(TestCase):

    def test_this_week(self):
        start_date, end_date = views_time_frames.this_week()
        self.assertEqual(start_date.weekday(), 0)  # check if start date is a monday
        self.assertEqual(end_date.weekday(), 6)  # check if end date is a sunday
        self.assertTrue(start_date <= end_date)  # check if start date is earlier than end date

        custom_start = datetime(2022, 10, 17)
        custom_end = datetime(2022, 10, 23)
        start_date, end_date = views_time_frames.this_week(start_date=custom_start, end_date=custom_end)
        self.assertEqual(start_date, custom_start)  # check if custom start date is used
        self.assertEqual(end_date, custom_end)  # check if custom end date is used

    def test_past_week(self):
        start_date, end_date = views_time_frames.past_week()
        self.assertEqual(start_date.weekday(), end_date.weekday())  # check if start and end date are on the same weekday
        self.assertTrue(start_date <= end_date)  # check if start date is earlier than end date

        custom_start = datetime(2022, 10, 10)
        custom_end = datetime(2022, 10, 16)
        start_date, end_date = views_time_frames.past_week(start_date=custom_start, end_date=custom_end)
        self.assertEqual(start_date, custom_start)  # check if custom start date is used
        self.assertEqual(end_date, custom_end)  # check if custom end date is used

    def test_next_week(self):
        # Test the function without any arguments
        start_date = datetime.now()
        end_date = views_time_frames.next_week()
        self.assertEqual(end_date.weekday(), start_date.weekday()-1) # if today is Monday, then end_date = Sunday, if today is Tuesday, then end_date = Monday
        self.assertTrue(end_date > start_date)

    def test_this_month(self):
        start_date, end_date = views_time_frames.this_month()
        self.assertEqual(start_date.day, 1)  # check if start date is the first day of the month
        self.assertTrue(start_date <= end_date)  # check if start date is earlier than end date

        custom_start = datetime(2022, 10, 1)
        custom_end = datetime(2022, 10, 31)
        start_date, end_date = views_time_frames.this_month(start_date=custom_start, end_date=custom_end)
        self.assertEqual(start_date, custom_start)  # check if custom start date is used
        self.assertEqual(end_date, custom_end)  # check if custom end date is used

    def test_past_month(self):
        start_date, end_date = views_time_frames.past_month()
        self.assertTrue(start_date <= end_date)  # check if start date is earlier than end date

        custom_start = datetime(2022, 9, 1)
        custom_end = datetime(2022, 9, 30)
        start_date, end_date = views_time_frames.past_month(start_date=custom_start, end_date=custom_end)
        self.assertEqual(start_date, custom_start)  # check if custom start date is used
        self.assertEqual(end_date, custom_end)  # check if custom end date is used

    def test_next_month(self):
        start_date = datetime.now().replace(hour=0, minute=0, second=0)
        end_date = views_time_frames.next_month(start_date)
        self.assertEqual(end_date.hour, 0) # test that the end date is at midnight
        self.assertGreater(end_date.month, start_date.month) # test that the end date is in the next month

    def test_this_year(self):
        start_date, end_date = views_time_frames.this_year()
        self.assertEqual(start_date, datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0))
        self.assertEqual(end_date, start_date.replace(month=12, day=31))

    def test_past_year(self):
        start_date, end_date =  views_time_frames.past_year()
        self.assertEqual(end_date, datetime.now().replace(hour=0, minute=0, second=0))
        self.assertEqual(start_date, end_date.replace(month=1, day=1) - timedelta(days=365))

    def test_past_months(self):
        num_months = 3
        months =  views_time_frames.past_months(num_months)
        self.assertEqual(len(months), num_months)
        for start_date, end_date, session in months:
            self.assertLessEqual(start_date, end_date)
            self.assertLessEqual(end_date, session)

    def test_past_months_from_today(self):
        num_months = 3
        months =  views_time_frames.past_months_from_today(num_months)
        self.assertEqual(len(months), num_months)
        for start_date, end_date, session in months:
            self.assertLessEqual(start_date, end_date)
            self.assertLessEqual(end_date, session)

    def test_past_weeks_from_today(self):
        num_weeks = 3
        weeks =  views_time_frames.past_weeks_from_today(num_weeks)
        self.assertEqual(len(weeks), num_weeks)
        for start_date, end_date, session in weeks:
            self.assertLessEqual(start_date, end_date)
            self.assertLessEqual(end_date, session)
        


   

       










