from django.test import TestCase
from css.models import *

# class FacultyCoursePreferences(models.Model):
#     faculty = models.ForeignKey(CUser, on_delete = models.CASCADE)
#     course = models.ForeignKey(Course, on_delete = models.CASCADE)
#     rank = models.IntegerField(default = 0)

#     @classmethod
#     def create(faculty, course, rank):
#         course_pref = cls(
#             faculty=faculty,
#             course=course,
#             rank=rank)
#         course_pref.save()
#         return course_pref

#     @classmethod
#     def get_faculty_pref(cls, faculty):
#         entries = cls.objects.filter(faculty='faculty')
#         #join the course ID to the course table
#         course_arr = {}
#         i = 0
#         for entry in entries:
#             course_id = entry.value(course)
#             #course_obj holds the entry in the table in the course table
#             course_obj = Course.objects.get(id=course_id)
#             course_arr[course_obj.rank] = course_obj.course_name
#         course_arr.sort()
#         return course_arr.values()

class FacultyCoursePreferencesTestCase(TestCase):
    def setUp(self):
    	faculty = CUser.create('makennajohnstone@gmail.com', '', 'faculty','Makenna','Johnstone')
    	course = Course.create('CPE 309', 'computers, projector','Software Engineering II')
    	FacultyCoursePreferences(faculty,course,3)

 	#enter a faculty member and return a list of the course objects and their ranks
    def test_get_faculty(self):
    	faculty = CUser.get_faculty('makennajohnstone@gmail.com')
    	faculty_pref = FacultyCoursePreferences.objects.get(faculty=faculty)
    	self.assertEquals(FacultyCoursePreferences.faculty.email, 'makennajohnstone@gmail.com')
		#course = Course.objects.get(name='CPE 309')