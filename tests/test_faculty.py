from django.test import TestCase
from css.models import *
import MySQLdb

class FacultyTestCase(TestCase):
    # Utility Functions 
    def create_faculty(self, email='email@email.com', password='password',
                       user_type='faculty'):
        return CUser.objects.create_cuser(email, password, user_type)

    def get_faculty(self):
        return CUser.objects.get_faculty()
    
    # @begin test
    def test_valid_faculty(self):     
        faculty = self.create_faculty()
        self.assertTrue(isinstance(faculty, CUser))
        self.assertEqual(faculty.user.email, 'email@email.com')
        self.assertEqual(faculty.user.password, 'password')
        self.assertEqual(faculty.user_type, 'faculty')
        faculty.delete()

    def test_empty_email(self):
        self.assertRaises(ValueError, self.create_faculty(email=''))

    def test_invalid_email(self):     
        self.assertRaises(ValueError, self.create_faculty(email='email'))

    def test_empty_password(self):     
        self.assertRaises(ValueError, self.create_faculty(password=''))

    # @TODO once password validation is defined, test it here
    #def test_invalid_password(self):
    #    pass

    def test_invalid_user_type(self):
        self.assertRaises(ValueError, self.create_faculty(user_type='aaa'))

    def test_filter_faculty_1(self):
        faculty1 = self.create_faculty(email='faculty1@email.com',
                                  user_type='faculty')
        faculty2 = self.create_faculty(email='faculty2@email.com',
                                  user_type='scheduler')
        faculty_list = self.get_faculty()
        self.assertTrue(faculty1 in faculty_list)
        self.assertTrue(faculty2 not in faculty_list)
        faculty1.delete()
        faculty2.delete()

    def test_filter_faculty_2(self):
        faculty1 = self.create_faculty(email='faculty1@email.com',
                                  user_type='scheduler')
        faculty2 = self.create_faculty(email='faculty2@email.com',
                                  user_type='scheduler')
        self.assertTrue(not self.get_faculty()) 
        faculty1.delete()
        faculty2.delete()


    def test_duplicate_faculty(self):
        faculty1 = self.create_faculty(email='faculty@email.com')
        self.assertRaises(MySQLdb.IntegrityError, 
                         self.create_faculty(email='faculty@email.com'))
        #self.assertEqual(cm.exception.error_code, 1062) #duplicate entry code


