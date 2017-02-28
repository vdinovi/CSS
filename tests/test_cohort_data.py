from django.test import TestCase
from django.core.exceptions import ValidationError
from css.models import *

class CohortDataTestCase(TestCase): 

    def setUp(self):
        Course.create(name="Total", equipment_req="", description="")
        Course.create(name="CPE 101", equipment_req="", description="Fundamentals of CS 1")
        Course.create(name="CPE 102", equipment_req="Table", description="Fundamentals of CS 2")
        Course.create(name="CPE 103", equipment_req="2 Chairs", description="Fundamentals of CS 3")
        Schedule.create(academic_term="Fall 2017", state="active")
        Schedule.create(academic_term="Winter 2017", state="active")

    def tearDown(self):
        Course.get_course(name="Total").delete()
        Course.get_course(name="CPE 101").delete()
        Course.get_course(name="CPE 102").delete()
        Course.get_course(name="CPE 103").delete()
        Schedule.get_schedule(term_name="Fall 2017").delete()
        Schedule.get_schedule(term_name="Winter 2017").delete()
    
    def test_new_cohort_entry_1(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        course = Course.get_course(name="CPE 101")
        cohort_data = CohortData.create(schedule=schedule, course=course, major="CSC",
                                        freshman=1, junior=2)

        self.assertEqual(cohort_data.schedule.id, schedule.id)
        self.assertEqual(cohort_data.course.id, course.id)
        self.assertEqual(cohort_data.major, "CSC")
        self.assertEqual(cohort_data.freshman, 1)
        self.assertEqual(cohort_data.sophmore, 0)
        self.assertEqual(cohort_data.junior, 2)
        self.assertEqual(cohort_data.senior, 0)

    def test_new_cohort_entry_2(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        course = Course.get_course(name="CPE 102")
        cohort_data = CohortData.create(schedule=schedule, course=course, major="SE",
                                        freshman=3, sophmore=2, junior=1, senior=0)
        self.assertEqual(cohort_data.schedule.id, schedule.id)
        self.assertEqual(cohort_data.course.id, course.id)
        self.assertEqual(cohort_data.major, "SE") 
        self.assertEqual(cohort_data.freshman, 3)
        self.assertEqual(cohort_data.sophmore, 2)
        self.assertEqual(cohort_data.junior, 1)
        self.assertEqual(cohort_data.senior, 0)

    def test_new_cohort_entry_2(self):
        schedule1 = Schedule.get_schedule(term_name="Fall 2017")
        schedule2 = Schedule.get_schedule(term_name="Winter 2017")
        course = Course.get_course(name="CPE 102")
        cohort_data1 = CohortData.create(schedule=schedule1, course=course, major="SE",
                                        freshman=3, sophmore=2, junior=1, senior=0)
        cohort_data2 = CohortData.create(schedule=schedule2, course=course, major="CPE",
                                        freshman=3, sophmore=2, junior=1, senior=0)
        self.assertEqual(cohort_data1.schedule.id, schedule1.id)
        self.assertEqual(cohort_data2.schedule.id, schedule2.id)


    def test_new_cohort_entry_4(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        course1 = Course.get_course(name="CPE 101")
        course2 = Course.get_course(name="CPE 102")
        course3 = Course.get_course(name="CPE 103")
        cohort_data1 = CohortData.create(schedule=schedule, course=course1, major="SE")
        cohort_data2 = CohortData.create(schedule=schedule, course=course2, major="CSC",
                                        freshman=3, sophmore=2, junior=1, senior=0)
        cohort_data3 = CohortData.create(schedule=schedule, course=course3, major="CPE",
                                        freshman=999, sophmore=999, junior=999, senior=999)
        self.assertEqual(cohort_data1.schedule.id, schedule.id)
        self.assertEqual(cohort_data1.course.id, course1.id)
        self.assertEqual(cohort_data1.major, "SE") 
        self.assertEqual(cohort_data2.schedule.id, schedule.id)
        self.assertEqual(cohort_data2.course.id, course2.id)
        self.assertEqual(cohort_data2.major, "CSC") 
        self.assertEqual(cohort_data3.schedule.id, schedule.id)
        self.assertEqual(cohort_data3.course.id, course3.id)
        self.assertEqual(cohort_data3.major, "CPE") 
 
        self.assertEqual(cohort_data1.freshman, 0)
        self.assertEqual(cohort_data1.sophmore, 0)
        self.assertEqual(cohort_data1.junior, 0)
        self.assertEqual(cohort_data1.senior, 0)

        self.assertEqual(cohort_data2.freshman, 3)
        self.assertEqual(cohort_data2.sophmore, 2)
        self.assertEqual(cohort_data2.junior, 1)
        self.assertEqual(cohort_data2.senior, 0)

        self.assertEqual(cohort_data3.freshman, 999)
        self.assertEqual(cohort_data3.sophmore, 999)
        self.assertEqual(cohort_data3.junior, 999)
        self.assertEqual(cohort_data3.senior, 999)

    def test_get_cohort_data_1(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        course = Course.get_course(name="CPE 101")
        cohort_data = CohortData.create(schedule=schedule, course=course, major="SE")
        exp_cohort_data = CohortData.get_cohort_data(schedule=schedule, course=course, major="SE")
        self.assertEqual(cohort_data.id, exp_cohort_data.id)
        self.assertEqual(cohort_data.course.id, exp_cohort_data.course.id)
        self.assertEqual(cohort_data.schedule.id, exp_cohort_data.schedule.id)
        self.assertEqual(cohort_data.major, exp_cohort_data.major)
        self.assertEqual(cohort_data.freshman, exp_cohort_data.freshman)
        self.assertEqual(cohort_data.sophmore, exp_cohort_data.sophmore)
        self.assertEqual(cohort_data.junior, exp_cohort_data.junior)
        self.assertEqual(cohort_data.senior, exp_cohort_data.senior)
 

    def test_new_cohort_total_1(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        cohort_total = CohortTotal.create(schedule=schedule, major="CSC") 
        self.assertEqual(cohort_total.schedule.id, schedule.id)
        self.assertEqual(cohort_total.major, "CSC")
        self.assertEqual(cohort_total.freshman, 0)
        self.assertEqual(cohort_total.sophmore, 0)
        self.assertEqual(cohort_total.junior, 0)
        self.assertEqual(cohort_total.senior, 0)

    def test_new_cohort_total_2(self):
        schedule = Schedule.get_schedule(term_name="Winter 2017")
        cohort_total = CohortTotal.create(schedule=schedule, major="CSC",
                                          freshman=997, sophmore=998, junior=999, senior=1000) 
        self.assertEqual(cohort_total.schedule.id, schedule.id)
        self.assertEqual(cohort_total.major, "CSC")
        self.assertEqual(cohort_total.freshman, 997)
        self.assertEqual(cohort_total.sophmore, 998)
        self.assertEqual(cohort_total.junior, 999)
        self.assertEqual(cohort_total.senior, 1000)

    def test_new_cohort_total_3(self):
        schedule1 = Schedule.get_schedule(term_name="Fall 2017")
        schedule2 = Schedule.get_schedule(term_name="Winter 2017")
        cohort_total1 = CohortTotal.create(schedule=schedule1, major="SE",
                                        freshman=3, sophmore=2, junior=1, senior=0)
        cohort_total2 = CohortTotal.create(schedule=schedule2, major="CPE",
                                        freshman=3, sophmore=2, junior=1, senior=0)
        self.assertEqual(cohort_total1.schedule.id, schedule1.id)
        self.assertEqual(cohort_total2.schedule.id, schedule2.id)

    def test_get_cohort_total_1(self):
        schedule = Schedule.get_schedule(term_name="Fall 2017")
        cohort_total = CohortTotal.create(schedule=schedule, major="CPE",
                                         freshman=1, senior=1)
        exp_cohort_total = CohortTotal.get_cohort_total(schedule=schedule, major="CPE")
        self.assertEqual(cohort_total.schedule.id, exp_cohort_total.schedule.id)
        self.assertEqual(cohort_total.major, exp_cohort_total.major)
        self.assertEqual(cohort_total.freshman, exp_cohort_total.freshman)
        self.assertEqual(cohort_total.sophmore, exp_cohort_total.sophmore)
        self.assertEqual(cohort_total.junior, exp_cohort_total.junior)
        self.assertEqual(cohort_total.senior, exp_cohort_total.senior)
 


 





 



 


