from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from css.models import *
from datetime import datetime


class SectionTestCase(TestCase): 
    def setUp(self):
        schedule = Schedule.create("Spring 2017", "active")
        course = Course.create("CPE101", "computers", "Fundamentals of Computer Science I")
        faculty = CUser.create("paula@calpoly.edu", "@1Testpass", "faculty", "Paula", "Ledgerwood")
        room = Room.create("14-156", "Graphics", 30, None, None)
        Section.create(
            schedule.academic_term, course.name, "10:00AM", "12:00PM", "MWF", 
            "paula@calpoly.edu", "14-156", 30, 0, 0, 
            'n', None, 'n', None)

    # def test_section_get_schedule1(self): 
    #     """ Test that schedule is retrieved properly """
    #     section = Section.Objects.get(schedule="Spring 2017")
    #     self.assertEquals(section.course.name, "CPE101")

    # def test_section_get_schedule2(self): 
    #     """ Test that creting section with nonexistant scheudule is raising error """
    #     self.assertRaises(ObjectDoesNotExist, Section.create,
    #         "Spring 2018", "CPE101", "10:00AM", "12:00PM", "MWF", 
    #         "paula@calpoly.edu", "14-156", 30, 0, 0, 
    #         'n', None, 'n', None
    #         )

    # def test_section_get_course1(self): 
    #     """ Test that course are retrieved properly """
    #     section = Section.Objects.get(course="CPE101")
    #     self.assertEquals(section.schedule.academic_term, "Spring 2017")

    # def test_section_get_course2(self): 
    #     """ Test that creting section with nonexistant course is raising error """
    #     self.assertRaises(ObjectDoesNotExist, Section.create,
    #         "Spring 2017", "CPE102", "10:00AM", "12:00PM", "MWF", 
    #         "paula@calpoly.edu", "14-156", 30, 0, 0, 
    #         'n', None, 'n', None)

    # def test_section_get_start_time(self): 
    #     """ Test that start_time in retrieved properly """
    #     section = Section.objects.get(start_time="10:00AM")
    #     self.assertEquals(section.end_time.strftime("%H:%M%p"), "12:00PM")

    # def test_section_get_end_time(self): 
    #     """ Test that end_time is retrieved properly """
    #     section = Section.objects.get(end_time="12:00PM")
    #     self.assertEquals(section.start_time.strftime("%H:%M%p"), "10:00AM")

    # def test_section_get_days1(self): 
    #     """ Test that days are retrieved properly """
    #     section = Section.objects.get(days="MWF")
    #     self.assertEquals(section.start_time.strftime("%H:%M%p"), "10:00AM")

    # def test_section_get_days2(self): 
    #     """ Test that days are retrieved properly """
    #     self.assertRaises(ObjectDoesNotExist, Section.objects.get, days="TR")

    def test_section_get_faculty(self): 
        """ Test that faculty are retrieved properly """
        section = Section.get_section(faculty="paula@calpoly.edu")
        self.assertEquals(section.course.name, "CPE101")

    def test_section_get_room(self): 
        """ Test that room assignment is retrieved properly """
        section = Section.get_section(room="14-156")
        self.assertEquals(section.room.name, "14-156")

    def test_section_get_section_capacity(self): 
        """ Test that section_capacity is retrieved properly """
        section = Section.objects.get(capacity=30)
        self.assertEquals(section.course.name, "CPE101")

    def test_section_get_students_enrolled(self): 
        """ Test that students_enrolled is retrieved properly """
        section = Section.objects.get(students_enrolled=0)
        self.assertEquals(section.course.name, "CPE101")

    def test_section_get_students_waitlisted(self): 
        """ Test that students_waitlisted is retrieved properly """
        section = Section.objects.get(students_waitlisted=0)
        self.assertEquals(section.course.name, "CPE101")

    def test_section_get_conflict1(self): 
        """ Test that conflict is retrieved properly """
        section = Section.objects.get(conflict='n')
        self.assertEquals(section.course.name, "CPE101")

    def test_section_get_conflict2(self): 
        """ Test that conflict retrieval raises does not exist error properly """
        self.assertRaises(ObjectDoesNotExist, Section.objects.get, conflict='y')

    def test_section_get_conflict_reason(self): 
        """ Test that conflict_reason is retrieved properly """
        section = Section.objects.get(conflict='n')
        self.assertEquals(section.conflict_reason, None)

    def test_section_get_fault(self): 
        """ Test that fault is retrieved properly """
        section = Section.objects.get(conflict='n')
        self.assertEquals(section.course.name, "CPE101")

    def test_section_get_fault_reason(self): 
        """ Test that fault_reason is retrieved properly """
        section = Section.objects.get(fault='n')
        self.assertEquals(section.fault_reason, None)

    #     #--------------- Filter Tests ----------------#
    # def test_section_filter_course_none(self):
    #     """ No sections match the name of one course we filter by. """
    #     course_filter = {'course': 'CPE103'}
    #     res_sections = Section.filter(course_filter)
    #     self.assertEquals(len(res_sections), 0)

    # def test_section_filter_course_one(self):
    #     """ One section matches the name of the one course we filter by. """
    #     course_filter = {'course': 'CPE101'}
    #     res_sections = Section.filter(course_filter)
    #     self.assertEquals(len(res_sections), 1)

    # def test_section_filter_course_multiple(self):
    #     """ Uses multiple courses as filter. Results in 3 sections."""
    #     course_filter = {'course': ('CPE101', 'CPE102')}   ## is this how filter would be fo multiple sections?
    #     res_sections = Section.filter(course_filter)
    #     self.assertEquals(len(res_sections), 3)

    # def test_section_filter_faculty_none(self):
    #     """ No sections match the name of one faculty we filter by. """
    #     faculty_filter = {'faculty': 'kearns'}
    #     res_sections = Section.filter(faculty_filter)
    #     self.assertEquals(len(res_sections), 0)

    # def test_section_filter_faculty_one(self):
    #     """ One section matches the name of the one faculty we filter by. """
    #     faculty_filter = {'course': 'CPE101'}
    #     res_sections = Section.filter(faculty_filter)
    #     self.assertEquals(len(res_sections), 1)

    # def test_section_filter_faculty_multiple(self):
    #     """ Uses multiple faculty as filter. Results in 3 sections."""
    #     faculty_filter = {'course': ('CPE101', 'CPE102')}
    #     res_sections = Section.filter(faculty_filter)
    #     self.assertEquals(len(res_sections), 3)

    # def test_section_filter_room_none(self):
    #     """ No sections match the name of one faculty we filter by. """
    #     room_filter = {'room': '14-001'}
    #     res_sections = Section.filter(room_filter)
    #     self.assertEquals(len(res_sections), 0)

    # def test_section_filter_room_one(self):
    #     """ One section matches the name of the one faculty we filter by. """
    #     room_filter = {'room': '14-157'}
    #     res_sections = Section.filter(room_filter)
    #     self.assertEquals(len(res_sections), 1)

    # def test_section_filter_room_multiple(self):
    #     """ Uses multiple faculty as filter. Results in 3 sections."""
    #     room_filter = {'room': ('14-157', '14-156')}
    #     res_sections = Section.filter(room_filter)
    #     self.assertEquals(len(res_sections), 3)

    # def test_section_time_invalid(self):
    #     """ 
    #         1. Start time is too early for department hours (8:00AM).
    #         2. End time is too late for department hours (5:00PM).
    #         3. Start time is after End time around noon.
    #         4. Start time is after End time.
    #     """
    #     # Earlier than start time
    #     time_filter = {'time': ('6:00AM', '7:00AM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 0)
    #     # Later than end time
    #     time_filter = {'time': ('10:00PM', '11:00PM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 0)
    #     # Start time later than end time over noon
    #     time_filter = {'time': ('1:00PM', '10:00AM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 0)
    #     # Start time later than end time
    #     time_filter = {'time': ('3:00PM', '2:00PM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 0)

    # def test_section_time_noon_midnight(self):
    #     """ Makes sure there are no errors when switching from am to pm. """
    #     time_filter = {'time': ('10:00AM', '1:00PM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 1)

    #     time_filter = {'time': ('10:00PM', '1:00AM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 0)

    # def test_section_time_success(self):
    #     """ Successful time filter returns 1 section. """
    #     time_filter = {'time': ('1:00PM', '3:00PM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 1)

    # def test_section_time_multiple(self):
    #     """ Successfully filters with 2 time filters. Returns 2 sections. """ 
    #     time_filter = {'time': (('9:00AM', '12:00PM'), ('1:00PM', '4:00PM'))}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 2)

    # def test_section_time_valid_none(self):
    #     """ Successful time filter results in 0 sections. """
    #     time_filter = {'time': ('4:00PM', '5:00PM')}
    #     res_sections = Section.filter(time_filter)
    #     self.assertEquals(len(res_sections), 0)

