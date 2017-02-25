from django.test import TestCase
from css.models import *

class FacultyTestCase(TestCase):
    # Utility Functions 
    @staticmethod
    def create_faculty(email='email@email.com', password='password#0',
                       user_type='faculty', first_name='blah', last_name='blah'):
        return CUser.create(email, password, user_type, first_name, last_name)

    @staticmethod
    def get_faculty(email=None):
        return CUser.get_faculty(email=email)

    @staticmethod
    def get_faculty_details(faculty):
        return FacultyDetails.objects.get(faculty=faculty)

    @staticmethod
    def get_all_faculty():
        return CUser.objects.filter(user_type='faculty')

    def verify_faculty_details(self, faculty, work_units, work_hours, changed_prefs):
        details = self.get_faculty_details(faculty)
        self.assertTrue(isinstance(details, FacultyDetails))
        self.assertEqual(details.faculty, faculty)
        self.assertEqual(details.target_work_units, work_units)
        self.assertEqual(details.target_work_hours, work_hours)
        self.assertEqual(details.changed_preferences, changed_prefs)

    def verify_faculty(self, faculty, email, password, first_name, last_name):
        # Verify User
        self.assertTrue(isinstance(faculty, CUser))
        self.assertEqual(faculty.user.email, email)
        self.assertTrue(faculty.user.check_password(password))
        self.assertEqual(faculty.user_type, 'faculty')
        self.assertEqual(faculty.user.first_name, first_name)
        self.assertEqual(faculty.user.last_name, last_name)
        # Verify Details
        self.verify_faculty_details(faculty, 0, 0, 'n')

    # Begin tests
    def test_valid_faculty(self):     
        faculty = self.create_faculty()
        self.verify_faculty(faculty, 'email@email.com', 'password#0', 'blah', 'blah')
        faculty.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email='email@email.com')

    def test_valid_faculty(self):     
        faculty1 = self.create_faculty(email='email1@email.com')
        faculty2 = self.create_faculty(email='email2@email.com')
        self.verify_faculty(faculty1, 'email1@email.com', 'password#0', 'blah', 'blah')
        self.verify_faculty(faculty2, 'email2@email.com', 'password#0', 'blah', 'blah')
        self.assertTrue(faculty1 in self.get_all_faculty())
        self.assertTrue(faculty2 in self.get_all_faculty())
        faculty1.delete()
        faculty2.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email='email@email.com')
        self.assertRaises(ObjectDoesNotExist, self.get_faculty_details, faculty=faculty1)

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

    # FacultyDetails
    def test_change_faculty_details(self):
        faculty = self.create_faculty()
        details = self.get_faculty_details(faculty)
        self.assertTrue(details is not False)
        self.assertEqual(details.changed_preferences, 'n')
        self.assertEqual(details.target_work_hours, 0)
        self.assertEqual(details.target_work_units, 0)
        details.change_details(new_work_units=4, new_work_hours=8)
        self.assertEqual(details.changed_preferences, 'y')
        self.assertEqual(details.target_work_hours, 8)
        self.assertEqual(details.target_work_units, 4)
        faculty.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_faculty_details, faculty=faculty)
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email="email@email.com")


    # DoesNotExist
    def test_invalid_faculty(self):
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email='aaaaaaaaa')

    def test_invalid_faculty(self):
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email='aaaaaaaaa')

    # Duplicate
    def test_duplicate_faculty(self):
        faculty1 = self.create_faculty()
        self.assertRaises(IntegrityError, self.create_faculty)

    # Delete
    def test_delete_faculty(self):
        faculty = self.create_faculty(email='email@email.com')
        details = self.get_faculty_details(faculty)
        self.assertTrue(faculty in self.get_all_faculty())
        faculty.delete()
        self.assertTrue(faculty not in self.get_all_faculty())
        self.assertRaises(ObjectDoesNotExist, self.get_faculty_details, faculty=faculty)
        self.assertRaises(ObjectDoesNotExist, self.get_faculty, email='email@email.com')



