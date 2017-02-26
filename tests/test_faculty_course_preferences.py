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
    	faculty = CUser.create('makennajohnstone@gmail.com', 'testPass1@', 'faculty', 'Makenna','Johnstone')
    	course1 = Course.create('CPE 308', 'computers, projector','Software Engineering I')
    	course2 = Course.create('CPE 309', 'computers, projector','Software Engineering II')
    	FacultyCoursePreferences.create(faculty, course1, None, 2)
    	FacultyCoursePreferences.create(faculty, course2, None, 1)

	#enter a faculty member and return a list of the course objects and their ranks
    def test_get_faculty_ranks(self):
    	faculty = CUser.get_faculty('makennajohnstone@gmail.com')
    	faculty_pref_list = FacultyCoursePreferences.get_course_list(faculty)
    	self.assertEquals(len(faculty_pref_list), 2)
    	self.assertEquals(faculty_pref_list[0][1], 'CPE 309')

    #deletes a faculty course preference model 
    def test_delete_preference(self):
    	course = Course.objects.get(name='CPE 309')
    	faculty = CUser.get_faculty('makennajohnstone@gmail.com')
    	faculty_pref = FacultyCoursePreferences.objects.get(course=course)
    	FacultyCoursePreferences.remove(faculty_pref)
    	faculty_pref_list = FacultyCoursePreferences.get_course_list(faculty)
    	self.assertEquals(len(faculty_pref_list), 1)
    	self.assertEquals(faculty_pref_list[0][1], 'CPE 308')



