from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from css.models import *


class SectionTestCase(TestCase): 
    def setUp(self):
        schedule = Schedule.create("Spring2017", "active")
        course = Course.create("CPE101", "computers", "Fundamentals of Computer Science I")
        faculty = CUser.create("paula@calpoly.edu", "@1Testpass", "faculty", "Paula", "Ledgerwood")
        room = Room.create("14-156", "Graphics", None, None, None)
        Section.create(
            schedule.academic_term, "CPE101", "10:00AM", "12:00PM", "MWF", 
            "paula@calpoly.edu", "14-156", 30, 0, 0, 
            'n', None, 'n', None
            )

    def test_section_get_schedule1(self): 
        """ Test that schedule is retrieved properly """
        section = Section.objects.get(schedule="Spring2017")
        self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_schedule2(self): 
    #     """ Test that creting section with nonexistant scheudule is raising error """
    #     self.assertRaises(Section.create(
    #         "Spring2018", "CPE101", "10:00AM", "12:00PM", "MWF", 
    #         "paula@calpoly.edu", "14-156", 30, 0, 0, 
    #         'n', None, 'n', None
    #         ), ObjectDoesNotExist)

    # def test_section_get_course1(self): 
    #     """ Test that course are retrieved properly """
    #     section = Section.objects.get(course="CPE101")
    #     self.assertEquals(section.schedule.academic_term, "Spring2017")

    # def test_section_get_course2(self): 
    #     """ Test that creting section with nonexistant course is raising error """
    #     self.assertRaises(Section.create(
    #         "Spring2017", "CPE102", "10:00AM", "12:00PM", "MWF", 
    #         "paula@calpoly.edu", "14-156", 30, 0, 0, 
    #         'n', None, 'n', None
    #         ), ObjectDoesNotExist)

    # def test_section_get_start_time(self): 
    #     """ Test that start_time in retrieved properly """
    #     section = Section.objects.get(start_time="10:00AM")
    #     self.assertEquals(section.end_time, "12:00PM")

    # def test_section_get_end_time(self): 
    #     """ Test that end_time is retrieved properly """
    #     section = Section.objects.get(end_time="12:00PM")
    #     self.assertEquals(section.start_time, "10:00AM")

    # def test_section_get_days1(self): 
    #     """ Test that days are retrieved properly """
    #     section = Section.objects.get(days="MWF")
    #     self.assertEquals(section.start_time, "10:00AM")

    # def test_section_get_days2(self): 
    #     """ Test that days are retrieved properly """
    #     section = Section.objects.get(days="TR")
    #     self.assertEquals(section, None)

    # def test_section_get_faculty(self): 
    #     """ Test that faculty are retrieved properly """
    #     section = Section.objects.get(faculty="paula@calpoly.edu")
    #     self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_room(self): 
    #     """ Test that room assignment is retrieved properly """
    #     section = Section.objects.get(room="14-156")
    #     room = Room.objects.get(section.room)
    #     self.assertEquals(room.name, "14-156")

    # def test_section_get_section_capacity(self): 
    #     """ Test that section_capacity is retrieved properly """
    #     section = Section.objects.get(capacity=30)
    #     self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_students_enrolled(self): 
    #     """ Test that students_enrolled is retrieved properly """
    #     section = Section.objects.get(students_enrolled=0)
    #     self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_students_waitlisted(self): 
    #     """ Test that students_waitlisted is retrieved properly """
    #     section = Section.objects.get(students_waitlisted=0)
    #     self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_conflict1(self): 
    #     """ Test that conflict is retrieved properly """
    #     section = Section.objects.get(conflict='n')
    #     self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_conflict2(self): 
    #     """ Test that conflict is retrieved properly """
    #     section = Section.objects.get(conflict='y')
    #     self.assertEquals(None)

    # def test_section_get_conflict_reason(self): 
    #     """ Test that conflict_reason is retrieved properly """
    #     section = Section.objects.get(conflict='n')
    #     self.assertEquals(section.conflict_reason, None)

    # def test_section_get_fault(self): 
    #     """ Test that fault is retrieved properly """
    #     section = Section.objects.get(conflict='n')
    #     self.assertEquals(section.course.course_name, "CPE101")

    # def test_section_get_fault_reason(self): 
    #     """ Test that fault_reason is retrieved properly """
    #     section = Section.objects.get(fault='n')
    #     self.assertEquals(section.fault_reason, None)

