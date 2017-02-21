from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from css.models import *


class SectionTestCase(TestCase): 
    def setUp(self):
        schedule = Schedule.create(academic_term="Spring 2017", state="active")
        course = Course.create("CPE101", "computers", "Fundamentals of Computer Science I")
        faculty = CUser.create("paula@calpoly.edu", "@1Testpass", "faculty", "Paula", "Ledgerwood")
<<<<<<< HEAD
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
=======
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
        Section.create(schedule3.academic_term, course3.name, "11:00AM", "12:00PM", "MWF", "paula@calpoly.edu", "14-157", 30, 0, 0, 'n', None, 'n', None)


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
    def test_section_filter_course_none(self):
        """ No sections match the name of one course we filter by. """
        course_filter = {'course': 'CPE103'}
        res_sections = Section.filter(course_filter)
        self.assertEquals(len(res_sections), 0)

    def test_section_filter_course_one(self):
        """ One section matches the name of the one course we filter by. """
        course_filter = {'course': 'CPE101'}
        res_sections = Section.filter(course_filter)
        self.assertEquals(len(res_sections), 1)

    def test_section_filter_course_multiple(self):
        """ Uses multiple courses as filter. Results in 3 sections."""
        course_filter = {'course': ('CPE101', 'CPE102')}   ## is this how filter would be fo multiple sections?
        res_sections = Section.filter(course_filter)
        self.assertEquals(len(res_sections), 3)

    def test_section_filter_faculty_none(self):
        """ No sections match the name of one faculty we filter by. """
        faculty_filter = {'faculty': 'kearns'}
        res_sections = Section.filter(faculty_filter)
        self.assertEquals(len(res_sections), 0)

    def test_section_filter_faculty_one(self):
        """ One section matches the name of the one faculty we filter by. """
        faculty_filter = {'course': 'CPE101'}
        res_sections = Section.filter(faculty_filter)
        self.assertEquals(len(res_sections), 1)

    def test_section_filter_faculty_multiple(self):
        """ Uses multiple faculty as filter. Results in 3 sections."""
        faculty_filter = {'course': ('CPE101', 'CPE102')}
        res_sections = Section.filter(faculty_filter)
        self.assertEquals(len(res_sections), 3)

    def test_section_filter_room_none(self):
        """ No sections match the name of one faculty we filter by. """
        room_filter = {'room': '14-001'}
        res_sections = Section.filter(room_filter)
        self.assertEquals(len(res_sections), 0)

    def test_section_filter_room_one(self):
        """ One section matches the name of the one faculty we filter by. """
        room_filter = {'room': '14-157'}
        res_sections = Section.filter(room_filter)
        self.assertEquals(len(res_sections), 1)

    def test_section_filter_room_multiple(self):
        """ Uses multiple faculty as filter. Results in 3 sections."""
        room_filter = {'room': ('14-157', '14-156')}
        res_sections = Section.filter(room_filter)
        self.assertEquals(len(res_sections), 3)

    def test_section_time_invalid(self):
        """ 
            1. Start time is too early for department hours (8:00AM).
            2. End time is too late for department hours (5:00PM).
            3. Start time is after End time around noon.
            4. Start time is after End time.
        """
        # Earlier than start time
        time_filter = {'time': ('6:00AM', '7:00AM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 0)
        # Later than end time
        time_filter = {'time': ('10:00PM', '11:00PM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 0)
        # Start time later than end time over noon
        time_filter = {'time': ('1:00PM', '10:00AM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 0)
        # Start time later than end time
        time_filter = {'time': ('3:00PM', '2:00PM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 0)

    def test_section_time_noon_midnight(self):
        """ Makes sure there are no errors when switching from am to pm. """
        time_filter = {'time': ('10:00AM', '1:00PM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 1)

        time_filter = {'time': ('10:00PM', '1:00AM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 0)

    def test_section_time_success(self):
        """ Successful time filter returns 1 section. """
        time_filter = {'time': ('1:00PM', '3:00PM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 1)

    def test_section_time_multiple(self):
        """ Successfully filters with 2 time filters. Returns 2 sections. """ 
        time_filter = {'time': (('9:00AM', '12:00PM'), ('1:00PM', '4:00PM'))}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 2)

    def test_section_time_valid_none(self):
        """ Successful time filter results in 0 sections. """
        time_filter = {'time': ('4:00PM', '5:00PM')}
        res_sections = Section.filter(time_filter)
        self.assertEquals(len(res_sections), 0)



>>>>>>> 742a392ea4ba636057838d294bdf98ec8cc76f1e

