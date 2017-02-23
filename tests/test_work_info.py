from django.test import TestCase
from django.db import IntegrityError
from css.models import *

class WorkInfoTestCase(TestCase):
	def setUp(self):
		course = Course.create('CPE 309', 'computers, projector','Software Engineering II')
		section_type = SectionType.create('Lecture')
		WorkInfo.create(course, section_type, 3, 5)
		
	def test_workinfo_get_course(self):
		course = Course.objects.get(name='CPE 309')
		work_info = WorkInfo.objects.get(course=course)
		self.assertEquals(work_info.course.name,'CPE 309')

	def test_workinfo_get_section_type(self):
		section_type = SectionType.objects.get(name='Lecture')
		work_info = WorkInfo.objects.get(section_type=section_type)
		self.assertEquals(work_info.section_type.name,'Lecture')

	def test_workinfo_get_work_units(self):
		work_info = WorkInfo.objects.get(work_units=3)
		self.assertEquals(work_info.work_units,3)

	def test_workinfo_get_work_hours(self):
		work_info = WorkInfo.objects.get(work_hours=5)
		self.assertEquals(work_info.work_hours,5)

	def test_duplicate_section(self):
		course = Course.objects.get(name='CPE 309')
		section_type = SectionType.objects.get(name='Lecture')
		self.assertRaises(IntegrityError, WorkInfo.create, course, section_type, 3, 5)

	def test_different_section_type(self):
		course = Course.objects.get(name='CPE 309')
		section_type = SectionType.create(name='Lab')
		WorkInfo.create(course, section_type, 3, 5)






