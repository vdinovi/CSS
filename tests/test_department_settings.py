from django.test import TestCase
from css.models import *
from css.settings import DEPARTMENT_SETTINGS
import os

class DepartmentSettingsTestCase(TestCase):
    current_settings = None

    def setUp(self):
        #self.current_settings = open("department_settings.json", "r").read()
        #os.remove("department_settings.json")
        pass

    def tearDown(self):
        #open("department_settings.json", "w").write(self.current_settings).close()
        pass
 
    def test_department_settings(self):
       pass 

 
