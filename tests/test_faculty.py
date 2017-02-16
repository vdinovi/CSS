from django.test import TestCase
from css.models import *


# @TODO Write tests for the following
# - Delete Faculty (success, failure-nonexistant, ...)
# 

class FacultyTestCase(TestCase):
    # Utility Functions 
    @staticmethod
    def create_faculty(email='email@email.com', password='password#0',
                       user_type='faculty'):
        return CUser.create(email, password, user_type)

    @staticmethod
    def get_faculty(email=None):
        return CUser.get_faculty(email=email)

    @staticmethod
    def get_all_faculty():
        return CUser.objects.filter(user_type='faculty')

    def verify_faculty(self, faculty, email, password):
        self.assertTrue(isinstance(faculty, CUser))
        self.assertEqual(faculty.user.email, email)
        self.assertTrue(faculty.user.check_password(password))
        self.assertEqual(faculty.user_type, 'faculty')

    # begin tests
    def test_valid_faculty(self):     
        faculty = self.create_faculty()
        self.verify_faculty(faculty, 'email@email.com', 'password#0')
        faculty.delete()

    # Email
    def test_valid_email_1(self):
        faculty = self.create_faculty(email='vito.dinovi@gmail.com')
        self.assertEqual(faculty.user.email, 'vito.dinovi@gmail.com')
        faculty.delete()

    def test_valid_email_2(self):
        faculty = self.create_faculty(email='vdinovi@calpoly.edu')
        self.assertEqual(faculty.user.email, 'vdinovi@calpoly.edu')
        faculty.delete()

    def test_invalid_email_1(self):
        self.assertRaises(ValidationError, self.create_faculty, email='')

    def test_invalid_email_2(self):     
        self.assertRaises(ValidationError, self.create_faculty, email='email')

    def test_invalid_email_3(self):     
        self.assertRaises(ValidationError, self.create_faculty, email='@test.com')

    # Password
    def test_valid_password_1(self):
        faculty = self.create_faculty(password='1.aaAZaa')
        self.assertTrue(faculty.user.check_password('1.aaAZaa'))
        faculty.delete()

    def test_valid_password_2(self):
        faculty = self.create_faculty(password='u*1zz+F?T')
        self.assertTrue(faculty.user.check_password('u*1zz+F?T'))
        faculty.delete()

    def test_invalid_password_1(self):     
        self.assertRaises(ValidationError, self.create_faculty, password='')

    def test_invalid_password_2(self):
        self.assertRaises(ValidationError, self.create_faculty, password='aaaaaaaaaaaaaaaaaaaaaaaaaaaaa$1aa')

    def test_invalid_password_3(self):
        self.assertRaises(ValidationError, self.create_faculty, password='1$aaaaa')

    # User type
    def test_invalid_user_type(self):
        self.assertRaises(ValidationError, self.create_faculty, user_type='aaa')

    # Filter
    def test_filter_faculty_1(self):
        faculty1 = self.create_faculty(email='faculty1@email.com',
                                  user_type='faculty')
        faculty2 = self.create_faculty(email='faculty2@email.com',
                                  user_type='scheduler')
        faculty_list = self.get_all_faculty()
        self.assertTrue(faculty1 in faculty_list)
        self.assertTrue(faculty2 not in faculty_list)
        faculty1.delete()
        faculty2.delete()

    def test_filter_faculty_2(self):
        faculty1 = self.create_faculty(email='faculty1@email.com',
                                  user_type='scheduler')
        faculty2 = self.create_faculty(email='faculty2@email.com',
                                  user_type='scheduler')
        self.assertTrue(not self.get_all_faculty()) 
        faculty1.delete()
        faculty2.delete()

    # Duplicate
    def test_duplicate_faculty(self):
        faculty1 = self.create_faculty()
        self.assertRaises(IntegrityError, self.create_faculty)

    # Delete
    def test_delete_faculty(self):
        faculty = self.create_faculty(email='email@email.com')
        self.assertTrue(faculty in self.get_all_faculty())
        faculty.delete()
        self.assertTrue(faculty not in self.get_all_faculty())
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email='email@email.com')

