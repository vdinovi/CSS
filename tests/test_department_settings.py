from django.test import TestCase
from css.models import *
from settings import DEPARTMENT_SETTINGS

class DepartmentSettingsTestCase(TestCase):
    
    def test_department_settings(self):
        old = DEPARTMENT_SETTINGS.__dict__()
        print old
 
