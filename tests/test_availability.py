from django.test import TestCase
from django.core.exceptions import ValidationError
from css.models import *

class AvailabilityTestCase(TestCase): 
    # Utility Functions 
    def create_faculty(self, email='email@email.com', password='password#0',
                       user_type='faculty', first_name='blah', last_name='blah'):
        return CUser.create(email, password, user_type, first_name, last_name)

    def setUp(self):
        self.create_faculty()

    def test_create_faculty(self):
        self.assertEquals(CUser.get_faculty(email="email@email.com").user_type, "faculty")

    def test_valid_availability1(self):
        availability = Availability.create("email@email.com", "MWF", "10:00", "AM", "12:00", "PM", "available")
        self.assertEquals(availability.days_of_week, "MWF")
    
    def test_valid_availability2(self):
        availability = Availability.create("email@email.com", "MWF", "10:00", "PM", "12:00", "AM", "available")
        self.assertEquals(availability.days_of_week, "MWF")

    def test_valid_availability3(self):
        availability = Availability.create("email@email.com", "TR", "10:00", "PM", "12:00", "PM", "preferred")
        self.assertEquals(availability.days_of_week, "TR")

    def test_valid_availability4(self):
        availability = Availability.create("email@email.com", "TR", "10:00", "AM", "12:00", "AM", "unavailable")
        self.assertEquals(availability.level, "unavailable")
        
    def test_availability_invalid_faculty_id(self):
        self.assertRaises(ObjectDoesNotExist, Availability.create, "email_unique@email.com", None, None, None, None, None, None)

    def test_availability_invalid_days_of_week(self):
        self.assertRaises(ValidationError, Availability.create, "email@email.com", "HELLO", None, None, None, None, None)

    def test_availability_invalid_start_time(self):
        self.assertRaises(ValidationError, Availability.create, "email@email.com", "MWF", None, "PM", "12:00", "PM", "available")

    def test_availability_invalid_end_time(self):
        self.assertRaises(ValidationError, Availability.create, "email@email.com", "TR", "12:00", "AM" ,None, "PM", None)

    def test_availability_invalid_level1(self):
        self.assertRaises(ValidationError, Availability.create, "email@email.com", "MWF", "10:00", "PM", "12:00", "PM", None)

    def test_availability_invalid_level2(self):
        self.assertRaises(ValidationError, Availability.create, "email@email.com", "MWF", "10:00", "PM", "12:00", "AM", "ew")


