from django.test import TestCase
from css.models import *

class SectionTypeTestCase(TestCase):

    def test_create_section_type_successful(self):
    	""" Expects a successful creation of a section type. """
    	SectionType.objects.create(section_type="Lecture")
        section = SectionType.objects.get(section_type="Lecture")
        self.assertEqual(section.section_type, "Lecture")

    def test_section_type_too_long(self):
    	""" Creates a section type with a name that is too long, expects an error. """
    	self.assertRaises(ValidationError, SectionType.create, "SectionTypeNameTooManyCharacters1")

    def test_valid_delete_section_type(self):
        st = SectionType.objects.create(section_type="Lab")
        self.assertTrue(SectionType.objects.get(section_type="lab"))
        st.delete()
        self.assertRaises(ObjectDoesNotExist, SectionType.objects.get, section_type="lab")

