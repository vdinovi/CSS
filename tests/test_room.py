from django.test import TestCase
from css.models import *

class RoomTestCase(TestCase): 
    def setUp(self):
        # room with all attributes defined
        Room.objects.create(name="14-255",
                            description="Graphics lab",
                            capacity=35,
                            notes="blah", 
                            equipment="whiteboard, computers, projector")
        # room without equipment defined
        Room.objects.create(name="180-101",
                            description="Chemistry lab",
                            capacity=25,
                            notes="bleh")
        # room with out notes defined
        Room.objects.create(name="4-111",
                            description="Engineering IV",
                            capacity=20,
                            equipment="whiteboard, large tables")

    def test_room_get_name(self): 
        """ Test that names are retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.get_name(), "14-255")
        self.assertEqual(chem.get_name(), "180-101")
        self.assertEqual(eng.get_name(), "4-111")

    def test_room_set_name(self): 
        """ Test that names are set properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        graphics.name = "14-256"
        chem.name = "180-102"
        eng.name = "4-112"
        graphics.save()
        chem.save()
        eng.save()
        self.assertEqual(graphics.get_name(), "14-256")
        self.assertEqual(chem.get_name(), "180-102")
        self.assertEqual(eng.get_name(), "4-112")

    def test_room_get_capacity(self):
        """ Test that capacity is retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.get_capacity(), 35)
        self.assertEqual(chem.get_capacity(), 25)
        self.assertEqual(eng.get_capacity(), 20)

    def test_room_set_capacity(self):
        """ Test that capacity is retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.get_capacity(), 35)
        self.assertEqual(chem.get_capacity(), 25)
        self.assertEqual(eng.get_capacity(), 20)

    def test_room_get_description(self):
        """ Test that description is retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.get_description(), "Graphics lab")
        self.assertEqual(chem.get_description(), "Chemistry lab")
        self.assertEqual(eng.get_description(), "Engineering IV")

    def test_room_get_notes(self):
        """ Test that notes are retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.get_notes(), "blah")
        self.assertEqual(chem.get_notes(), "bleh")
        self.assertEqual(eng.get_notes(), None)

    def test_room_get_equipment(self):
        """ Test that equipment retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.get_equipment(), "whiteboard, computers, projector")
        self.assertEqual(chem.get_equipment(), None)
        self.assertEqual(eng.get_equipment(), "whiteboard, large tables")


