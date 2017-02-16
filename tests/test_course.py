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

    def tearDown(self):
        for course in Course.objects.filter().all():
            course.delete()
        self.assertTrue(not Course.objects.filter())

    def test_course_name(self):
        """ Course name is retrieved correctly. """
        course1 = Course.get_course(course_name="CPE 101")
        course2 = Course.get_course(course_name="CPE 102")
        course3 = Course.get_course(course_name="CPE 103")
        course4 = Course.get_course(course_name="CPE 309")
        self.assertEqual(course1.course_name, "CPE 101")
        self.assertEqual(course2.course_name, "CPE 102")
        self.assertEqual(course3.course_name, "CPE 103")
        self.assertEqual(course4.course_name, "CPE 309")

    def test_equipment_req(self):
        """ Equipment requirements are correctly retrieved. """
        course1 = Course.get_course(course_name="CPE 101")
        course2 = Course.get_course(course_name="CPE 102")
        course3 = Course.get_course(course_name="CPE 103")
        course4 = Course.get_course(course_name="CPE 309")
        self.assertEqual(course1.equipment_req, "table")
        self.assertEqual(course2.equipment_req, None)
        self.assertEqual(course3.equipment_req, "computer")
        self.assertEqual(course4.equipment_req, None)


    def test_description(self):
        """ Course description is correctly retrieved. """
        course1 = Course.get_course(course_name="CPE 101")
        course2 = Course.get_course(course_name="CPE 102")
        course3 = Course.get_course(course_name="CPE 103")
        course4 = Course.get_course(course_name="CPE 309")
        self.assertEqual(course1.description, "cool course")
        self.assertEqual(course2.description, None)
        self.assertEqual(course3.description, None)
        self.assertEqual(course4.description, "kearns")

    def test_course_name_too_long(self):
        """ Invalid course name raises validation error. """
        self.assertRaisesRegexp(ValidationError, "Invalid data for course creation.", Course.create, "CourseNameTooLong", None, None)

    # Test setters
    def test_set_equipment_req(self):
        course = Course.get_course(course_name="CPE 101")
        course.set_equipment_req("new table")
        course = Course.get_course(course_name="CPE 101")
        self.assertEqual(course.equipment_req, "new table")

    def test_set_description(self):
        course = Course.get_course(course_name="CPE 101")
        course.set_description("new description")
        course = Course.get_course(course_name="CPE 101")
        self.assertEqual(course.description, "new description")

    # Delete tests
    def test_delete_course(self):
        courses = Course.get_all_courses().all()
        self.assertEqual(len(courses), 4)
        courses[0].delete()
        courses[1].delete()
        courses[2].delete()
        courses[3].delete()
        self.assertEqual(Course.get_all_courses().count(), 0)
