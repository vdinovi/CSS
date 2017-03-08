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
        Section.create(1,
            schedule1.academic_term, course101.name, type1.name, "10:00", "12:00", "MWF", 
            "paula@calpoly.edu", "14-156", 30, 0, 0, 
            "n", None, "n", None)
        Section.create(2,
            schedule2.academic_term, course102.name, type2.name, "12:00", "14:00", "MWF", 
            "sigal@calpoly.edu", "14-157", 50, 0, 0, 
            "n", None, "y", "room")

    def test_faculty_conflict(self):
        new_section = Section.create(3,
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

        conflicts = SectionConflict.objects.all()
        for conflict in conflicts:
            print "----Conflict----"
            print str(conflict.section1.section_num) + " " + conflict.section1.course.name + " " + conflict.section1.section_type.name
            print str(conflict.section2.section_num) + " " + conflict.section2.course.name + " " + conflict.section2.section_type.name
            print conflict.conflict_reason
            print "----------------"


    def test_room_conflict(self):
        new_section = Section.create(4,
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "sigal@calpoly.edu", "14-156", 30, 0, 0,
            "n", None, "n", None)
        Conflicts(new_section)
        existing_section = Section.get_section(course="CPE101")
        self.assertEquals(str(existing_section.conflict), 'y')
        self.assertEquals(str(existing_section.conflict_reason), "room")
        self.assertEquals(1, len(SectionConflict.objects.all()))

        conflicts = SectionConflict.objects.all()
        for conflict in conflicts:
            print "----Conflict----"
            print str(conflict.section1.section_num) + " " + conflict.section1.course.name + " " + conflict.section1.section_type.name
            print str(conflict.section2.section_num) + " " + conflict.section2.course.name + " " + conflict.section2.section_type.name
            print conflict.conflict_reason
            print "----------------"

    def test_get_faculty_conflict(self):
        section1 = Section.get_section(course="CPE101")
        section2 = Section.get_section(course="CPE102")
        section3 = Section.create(4,
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "sigal@calpoly.edu", "14-156", 30, 0, 0,
            "n", None, "n", None)
        section4 = Section.create(5,
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "sigal@calpoly.edu", "14-156", 30, 0, 0,
            "n", None, "n", None)
        section5 = Section.create(6,
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "sigal@calpoly.edu", "14-156", 30, 0, 0,
            "n", None, "n", None)
        section6 = Section.create(7,
            "Spring 2017", "CPE102", "Lab", "10:00", "11:00", "MWF",
            "sigal@calpoly.edu", "14-156", 30, 0, 0,
            "n", None, "n", None)

        SectionConflict.create(section1, section2, 'faculty')
        SectionConflict.create(section2, section3, 'faculty')
        SectionConflict.create(section4, section2, 'faculty')
        SectionConflict.create(section1, section4, 'faculty')
        SectionConflict.create(section3, section2, 'room')
        SectionConflict.create(section1, section3, 'room')

        fconflicts1 = Section.get_faculty_conflicts(section1)
        fconflicts2 = Section.get_faculty_conflicts(section2)
        fconflicts3 = Section.get_faculty_conflicts(section3)
        fconflicts4 = Section.get_faculty_conflicts(section4)
        rconflicts1 = Section.get_room_conflicts(section1)
        rconflicts2 = Section.get_room_conflicts(section2)
        rconflicts3 = Section.get_room_conflicts(section3)
        rconflicts4 = Section.get_room_conflicts(section4)

        # Checks that lengths are all equal
        self.assertEquals(len(fconflicts1), 2)
        self.assertEquals(len(fconflicts2), 3)
        self.assertEquals(len(fconflicts3), 1)
        self.assertEquals(len(fconflicts4), 2)
        self.assertEquals(len(rconflicts1), 1)
        self.assertEquals(len(rconflicts2), 1)
        self.assertEquals(len(rconflicts3), 2)
        self.assertEquals(len(rconflicts4), 0)
        








