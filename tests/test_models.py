from django.test import TestCase
from css.models import *

# test User, Section, Room, and FacultyWorkInfo

class FacultyTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

class RoomTestCase(TestCase): 
    def setUp(self):
        Room.objects.create(name="14-255",
                            description="Graphics lab",
                            capacity=35,
                            notes="blah", 
                            equipment="whiteboard, computers, projector")
        Room.objects.create(name="180-101",
                            description="Chemistry lab",
                            capacity=25,
                            notes="bleh", 
                            equipment="whiteboard, microscopes, sinks")

    def test_room_names(self): 
        # test that 
        graphics = Room.Objects.get(name="14-255")

