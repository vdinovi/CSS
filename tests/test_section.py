from django.test import TestCase
from django.core.exceptions import ValidationError
from css.models import *


class SectionTestCase(TestCase): 
    def setUp(self):
        schedule = Schedule.create(academic_term="Spring 2017", state="active")
        course = Course.create("CPE101", "computers", "Fundamentals of Computer Science I")
        faculty = CUser.create("paula@calpoly.edu", "@1Testpass", "faculty", "Paula", "Ledgerwood")
        room = Room.create("14-156", "Graphics", 0, None, None)
        Section.create(schedule.academic_term, course.name, "10:00AM", "12:00PM", "MWF", "paula@calpoly.edu", "14-156", 30, 0, 0, 'n', None, 'n', None)

        schedule2 = Schedule.create("Spring2017", "active")
        course2 = Course.create("CPE102", "computers", "Fundamentals of Computer Science II")
        faculty2 = CUser.create("paula2@calpoly.edu", "@2Testpass", "faculty", "Paula", "Ledgerwood")
        room2 = Room.create("14-156", "Graphics", None, None, None)
        Section.create(schedule2.academic_term, course2.name, "1:00PM", "3:00PM", "MWF", "paula@calpoly.edu", "14-156", 30, 0, 0, 'n', None, 'n', None)

        schedule3 = Schedule.create("Spring2017", "active")
        course3 = Course.create("CPE102", "computers", "Fundamentals of Computer Science I")
        faculty3 = CUser.create("paula3@calpoly.edu", "@3Testpass", "faculty", "Paula", "Ledgerwood")
        room3 = Room.create("14-157", "Graphics", None, None, None)
        Section.create(schedule3.academic_term, course3.name, "10:00AM", "12:00PM", "MWF", "paula@calpoly.edu", "14-157", 30, 0, 0, 'n', None, 'n', None)


    # @TODO paula
    # def test_section_get_schedule(self): 
    #     """ Test that schedule is retrieved properly """
    #     self.assertEquals(, None)

    # # @TODO
    # def test_section_get_course(self): 
    #     """ Test that course are retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_start_time(self): 
    #     """ Test that start_time in retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_end_time(self): 
    #     """ Test that end_time is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_days(self): 
    #     """ Test that days are retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_faculty(self): 
    #     """ Test that faculty are retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_room(self): 
    #     """ Test that room assignment is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_section_capacity(self): 
    #     """ Test that section_capacity is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_students_enrolled(self): 
    #     """ Test that students_enrolled is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_students_waitlisted(self): 
    #     """ Test that students_waitlisted is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_conflict(self): 
    #     """ Test that conflict is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_conflict_reason(self): 
    #     """ Test that conflict_reason is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_fault(self): 
    #     """ Test that fault is retrieved properly """
    #     self.assertEquals(None, None)

    # # @TODO
    # def test_section_get_fault_reason(self): 
    #     """ Test that fault_reason is retrieved properly """
    #     self.assertEquals(None, None)


        #--------------- Filter Tests ----------------#
    def test_section_filter_name(self):
        """ No sections match the name of course we filter by. """
        name_filter = {'course': 'CPE101'}
        res_sections = Section.filter(name_filter)
        self.assertEquals(len(res_sections), 1)

