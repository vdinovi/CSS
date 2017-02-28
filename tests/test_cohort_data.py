from django.test import TestCase
from django.core.exceptions import ValidationError
from css.models import *

class CohortDataTestCase(TestCase): 

    def setUp(self):
        Course.create(course="Total", equipment_req="", description="")
        Course.create(course="CPE 101", equipment_req="", description="Fundamentals of CS 1")
        Course.create(course="CPE 102", equipment_req="Table", description="Fundamentals of CS 2")
        Course.create(crouse="CPE 103", equipment_req="2 Chairs", description="Fundamentals of CS 3")
        Schedule.create(academic_term="Fall 2017")

    def tearDown(self):
        Course.get_course(name="Total").delete()
        Course.get_course(name="CPE 101").delete()
        Course.get_course(name="CPE 102").delete()
        Course.get_course(name="CPE 103").delete()
        Schedule.get_schedule(term_name="Fall 2017").delete()
    
    def test_new_cohort_entry_1(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        course = Course.get_course(name="CPE101")
        cohort_data = CohortData.create(schedule=schedule, course=course, major="CSC",
                                        freshman=1, freshman_total=2)
        self.assertTrue(cohort_data is CohortData.get_cohort_data(schedule=schedule, course=course, major="CSC"))

