from django.test import TestCase
from css.models import *

class AvailabilityTestCase(TestCase): 
    # Utility Functions 
    def create_faculty(self, email='email@email.com', password='password#0',
                       user_type='faculty'):
        return CUser.objects.create_cuser(email, password, user_type)

    def setUp(self):
        create_faculty()

    def tearDown(self):
        CUser.objects.get(email="email@email.com").delete()

    def test_availability_invalid_faculty_id(self):
        self.assertRaises(ValidationError, Availability.create("email_unique@email.com", None, None, None, None))

    def test_availability_invalid_days_of_week(self):
        self.assertRaises(ValidationError, Availability.create("email@email.com", "HELLO", None, None, None))

    def test_availability_invalid_start_time(self):
        # TODO: add actual test for invalid start time
        self.assertRaises(ValidationError, Availability.create("email@email.com", "MWF", None, None, None))

    def test_availability_invalid_end_time(self):
        # TODO: add actual test for invalid end time
        self.assertRaises(ValidationError, Availability.create("email@email.com", "TR", None, None, None))

    def test_availability_invalid_level(self):
        # TODO: add actual test for invalid level
        self.assertRaises(ValidationError, Availability.create("email@email.com", "MWF", , None, None))


