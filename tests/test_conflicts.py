from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from css.models import *
from datetime import datetime
from css.scheduling import Conflicts

class ConflictsTestCase(TestCase):
    def setUp(self):
        schedule1 = Schedule.create("Spring 2017", "active")
        schedule2 = Schedule.create("Winter 2017", "approved")
        type1 = SectionType.create("Lecture")
        type2 = SectionType.create("Lab")
        course101 = Course.create("CPE101", "computers", "Fundamentals of Computer Science I")
        course102 = Course.create("CPE102", "computers", "Fundamentals of Computer Science II")
        faculty1 = CUser.create("paula@calpoly.edu", "@1Testpass", "faculty", "Paula", "Ledgerwood")
        faculty2 = CUser.create("sigal@calpoly.edu", "@1Testpass", "faculty", "Sigal", "Shaul")
        room = Room.create("14-156", "Graphics", 30, None, None)
        room = Room.create("14-157", "Security", 30, None, None)
        Section.create(
            schedule1.academic_term, course101.name, type1.name, "10:00", "12:00", "MWF", 
            "paula@calpoly.edu", "14-156", 30, 0, 0, 
            "n", None, "n", None)
        Section.create(
            schedule2.academic_term, course102.name, type2.name, "12:00", "14:00", "MWF", 
            "sigal@calpoly.edu", "14-157", 50, 0, 0, 
            "n", None, "y", "room")

    def test_faculty_conflict(self):
        new_section = Section.create(
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "paula@calpoly.edu", "14-157", 30, 0, 0,
            "n", None, "n", None)
        sections = Section.objects.all()
        print "------------BEFORE------------:"
        for section in sections:
            print section.schedule.academic_term + " " + section.course.name + " " + section.conflict + " " + str(section.conflict_reason)
        print '-------------------------------'
        Conflicts(new_section)
        existing_section = Section.get_section(course="CPE101")
        sections = Section.objects.all()
        print "------------AFTER------------:"
        for section in sections:
            print section.schedule.academic_term + " " + section.course.name + " " + section.conflict + " " + str(section.conflict_reason)
        self.assertEquals(str(existing_section.conflict), 'y')
        self.assertEquals(str(existing_section.conflict_reason), "faculty")

    def test_room_conflict(self):
        new_section = Section.create(
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "sigal@calpoly.edu", "14-156", 30, 0, 0,
            "n", None, "n", None)
        Conflicts(new_section)
        existing_section = Section.get_section(course="CPE101")
        self.assertEquals(str(existing_section.conflict), 'y')
        self.assertEquals(str(existing_section.conflict_reason), "room")
        self.assertEquals(1, len(SectionConflict.objects.all()))



