from django.test import TestCase
from css.models import *

class ScheduleTestCase(TestCase):
    def setUp(self):
        Schedule.objects.create(academic_term="Fall 2017", state="active")
        Schedule.objects.create(academic_term="Winter 2017")

    def test_approve_schedule(self):
        """ Changes an active schedule to approved. """
        schedule = Schedule.objects.get(academic_term="Fall 2017")
        schedule.approve()
        self.assertEqual(schedule.state, "approved")

    def test_default_active_schedule(self):
        """ Creates a schedule with no state. Checking state defaults to active."""
        schedule = Schedule.objects.get(academic_term="Winter 2017")
        self.assertEqual(schedule.state, "active")

    def test_return_to_active_schedule(self):
        """ Changes an active schedule to approved and returns it to active. """
        schedule = Schedule.objects.get(academic_term="Winter 2017")
        schedule.approve()
        self.assertEqual(schedule.state, "approved")
        schedule.return_to_active()
        self.assertEqual(schedule.state, "active")

    def test_invalid_state(self):
        """ Checks that an invalid input for state raises an error. """
        self.assertRaises(ValidationError, Schedule.create, "Winter 2019", "invalid")
