from django.test import TestCase
from django.core.exceptions import ValidationError
from css.models import *


class SectionTestCase(TestCase): 
    def setUp(self):
        Section.objects.create()
        Sections.objects.create()
        Sections.objects.create()

    @TODO
    def test_section_get_schedule(self): 
        """ Test that schedule is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_course(self): 
        """ Test that course are retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_start_time(self): 
        """ Test that start_time in retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_end_time(self): 
        """ Test that end_time is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_days(self): 
        """ Test that days are retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_faculty(self): 
        """ Test that faculty are retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_room(self): 
        """ Test that room assignment is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_section_capacity(self): 
        """ Test that section_capacity is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_students_enrolled(self): 
        """ Test that students_enrolled is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_students_waitlisted(self): 
        """ Test that students_waitlisted is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_conflict(self): 
        """ Test that conflict is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_conflict_reason(self): 
        """ Test that conflict_reason is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_fault(self): 
        """ Test that fault is retrieved properly """
        self.assertEquals(None, None)

    @TODO
    def test_section_get_fault_reason(self): 
        """ Test that fault_reason is retrieved properly """
        self.assertEquals(None, None)

