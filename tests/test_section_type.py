from django.test import TestCase
from css.models import *

class SectionTypeTestCase(TestCase):

    def test_create_section_type_successful(self):
    	""" Expects a successful creation of a section type. """
    	SectionType.create("Lecture")
        section = SectionType.get_section_type(name="Lecture")
        self.assertEqual(section.name, "Lecture")

    def test_section_type_too_long(self):
    	""" Creates a section type with a name that is too long, expects an error. """
    	self.assertRaises(ValidationError, SectionType.create, "SectionTypeNameTooManyCharacters1")

    def test_valid_delete_section_type(self):
        st = SectionType.create("Lab")
        self.assertTrue(SectionType.get_section_type("lab"))
        st.delete()
        self.assertRaises(ObjectDoesNotExist, SectionType.objects.get, name="lab")

