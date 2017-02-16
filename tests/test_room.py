from django.test import TestCase
from django.core.exceptions import ValidationError
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
        self.assertEqual(graphics.name, "14-255")
        self.assertEqual(chem.name, "180-101")
        self.assertEqual(eng.name, "4-111")

    def test_room_set_name(self): 
        """ Test that names are set properly """
        graphics = Room.objects.get(name="14-255")
        graphics.name = "14-256"
        graphics.save()
        self.assertEqual(graphics.name, "14-256")

    def test_room_name_too_long(self):
        self.assertRaises(ValidationError, Room.create,"ThisNameIsTooLongForOurRoomNameAttribute", None, None, None, None)

    def test_room_get_capacity(self):
        """ Test that capacity is retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.capacity, 35)
        self.assertEqual(chem.capacity, 25)
        self.assertEqual(eng.capacity, 20)
        
    def test_room_set_capacity(self):
        """ Test that capacity is retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.capacity, 35)
        self.assertEqual(chem.capacity, 25)
        self.assertEqual(eng.capacity, 20)
        
    def test_room_capacity_too_long(self):
        self.assertRaises(ValidationError, Room.create, None, None, None, None, None)

    def test_room_get_description(self):
        """ Test that description is retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.description, "Graphics lab")
        self.assertEqual(chem.description, "Chemistry lab")
        self.assertEqual(eng.description, "Engineering IV")

    def test_room_set_description(self):
        """ Test that description is set properly """
        graphics = Room.objects.get(name="14-255")
        graphics.description = "Security lab"
        self.assertEqual(graphics.description, "Security lab")

    def test_room_description_too_long(self):
        self.assertRaises(ValidationError, Room.create, "ThisIsOurName", "DescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLong", None, None, None)

    def test_room_get_notes(self):
        """ Test that notes are retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.notes, "blah")
        self.assertEqual(chem.notes, "bleh")
        self.assertEqual(eng.notes, None)

    def test_room_set_notes(self):
        """ Test that notes are retrieved properly """
        eng = Room.objects.get(name="4-111")
        eng.notes = "This class is honors"
        eng.save()
        self.assertEqual(eng.notes, "This class is honors")

    def test_room_notes_too_long(self):
        self.assertRaises(ValidationError, Room.create, "ThisIsOurName2", None, None, "DescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLong", None)

    def test_room_get_equipment(self):
        """ Test that equipment retrieved properly """
        graphics = Room.objects.get(name="14-255")
        chem = Room.objects.get(name="180-101")
        eng = Room.objects.get(name="4-111")
        self.assertEqual(graphics.equipment, "whiteboard, computers, projector")
        self.assertEqual(chem.equipment, None)
        self.assertEqual(eng.equipment, "whiteboard, large tables")

    def test_room_equipment_too_long(self):
        self.assertRaises(ValidationError, Room.create, None, None, None, None, "DescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLongDescriptionIsWayTooLong")


