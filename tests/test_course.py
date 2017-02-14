from django.test import TestCase
from css.models import *

class CourseTestCase(TestCase):
    def setUp(self):

        # Course with all attributes defined.
        Course.objects.create(course_name="CPE 101",
                              equipment_req="table",
                              description="cool course")

        # Course with no equipment requirements and description.
        Course.objects.create(course_name="CPE 102")

        # Course with no description.
        Course.objects.create(course_name="CPE 103",
                              equipment_req="computer")

        # Course with no equipment requirements.
        Course.objects.create(course_name="CPE 309",
                              description="kearns")

    def test_course_name(self):
        """ Course name is retrieved correctly. """
        course1 = Course.objects.get(course_name="CPE 101")
        course2 = Course.objects.get(course_name="CPE 102")
        course3 = Course.objects.get(course_name="CPE 103")
        course4 = Course.objects.get(course_name="CPE 309")
        self.assertEqual(course1.course_name, "CPE 101")
        self.assertEqual(course2.course_name, "CPE 102")
        self.assertEqual(course3.course_name, "CPE 103")
        self.assertEqual(course4.course_name, "CPE 309")

    def test_equipment_req(self):
        """ Equipment requirements are correctly retrieved. """
        course1 = Course.objects.get(course_name="CPE 101")
        course2 = Course.objects.get(course_name="CPE 102")
        course3 = Course.objects.get(course_name="CPE 103")
        course4 = Course.objects.get(course_name="CPE 309")
        self.assertEqual(course1.equipment_req, "table")
        self.assertEqual(course2.equipment_req, None)
        self.assertEqual(course3.equipment_req, "computer")
        self.assertEqual(course4.equipment_req, None)


    def test_description(self):
        """ Course description is correctly retrieved. """
        course1 = Course.objects.get(course_name="CPE 101")
        course2 = Course.objects.get(course_name="CPE 102")
        course3 = Course.objects.get(course_name="CPE 103")
        course4 = Course.objects.get(course_name="CPE 309")
        self.assertEqual(course1.description, "cool course")
        self.assertEqual(course2.description, None)
        self.assertEqual(course3.description, None)
        self.assertEqual(course4.description, "kearns")

    def test_course_name_too_long(self):
        """ Invalid course name raises validation error. """
        self.assertRaisesRegexp(ValidationError, "Invalid data for course creation.", Course.create, "CourseNameTooLong", None, None)
