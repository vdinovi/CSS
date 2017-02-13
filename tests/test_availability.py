from django.test import TestCase
from css.models import *

class AvailabilityTestCase(TestCase): 
    # Utility Functions 
    def create_faculty(self, email='email@email.com', password='password#0',
                       user_type='faculty'):
        return CUser.objects.create_cuser(email, password, user_type)

    def test_availability_invalid_faculty_id(self):
        faculty = create_faculty()
        self.assertRaises(ValidationError, Availability.create("testunique@email.com", "BLAH", None, None, None))

    def test_availability_invalid_days_of_week(self):
        self.assertRaises(ValidationError, Availability.create())

    def test_availability_invalid_start_time(self):
        self.assertRaises(ValidationError, Availability.create())

    def test_availability_invalid_end_time(self):
        self.assertRaises(ValidationError, Availability.create())

    def test_availability_invalid_level(self):
        self.assertRaises(ValidationError, Availability.create())
