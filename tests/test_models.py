from django.test import TestCase
from css.models import *

# test User, Section, Room, and FacultyWorkInfo

class FacultyTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

class RoomTestCase(TestCase): 
    def setUp(self):
        Room.objects.create(name="14-255",
                            description="Graphics lab",
                            capacity=35,
                            notes="blah", 
                            equipment="whiteboard, computers, projector")
        Room.objects.create(name="180-101",
                            description="Chemistry lab",
                            capacity=25,
                            notes="bleh", 
                            equipment="whiteboard, microscopes, sinks")

    def test_room_names(self): 
        # test that 
        graphics = Room.objects.get(name="14-255")


class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(course_name="CPE 101",
                              equipment_req="table",
                              description="cool course")

    def test_course_name(self):
        course = Course.objects.get(course_name="CPE 101")
        self.assertEqual(course.get_name(), "CPE 101")

    def test_equipment_req(self):
        """ Equipment requirements are correctly retrieved. """
        course = Course.objects.get(course_name="CPE 101")
        self.assertEqual(course.get_equipment_req(), "table")

    def test_description(self):
        """ Course description is correctly retrieved. """
        course = Course.objects.get(course_name="CPE 101")
        self.assertEqual(course.get_description(), "cool course")    