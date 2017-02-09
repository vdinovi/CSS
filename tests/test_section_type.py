from django.test import TestCase
from css.models import *

class SectionTypeTestCase(TestCase):
    def setUp(self):
        SectionType.objects.create(section_type="Lecture")
        SectionType.objects.create(section_type="Lab")

    def test_create_section_type(self):
        section = SectionType.objects.get(section_type="Lecture")
        self.assertEqual(section.section_type, "Lecture")

