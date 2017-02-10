from django.test import TestCase
from css.models import *
from django.core.exceptions import ValidationError

class SectionTypeTestCase(TestCase):
    def setUp(self):
        SectionType.objects.create(section_type="Lecture")

    def test_create_section_type(self):
        section = SectionType.objects.get(section_type="Lecture")
        self.assertEqual(section.section_type, "Lecture")

    def test_section_type_too_long(self):
    	self.assertRaises(ValidationError, SectionType.objects.create, section_type="SectionTypeNameTooManyCharacters1")
