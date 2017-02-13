from django.test import TestCase
from css.models import *

class ScheduleTestCase(TestCase):
    def setUp(self):
        Schedule.objects.create(academic_term="Fall 2017", state="active")
        Schedule.objects.create(academic_term="Winter 2017")

    def test_finalize_schedule(self):
        schedule = Schedule.objects.get(academic_term="Fall 2017")
        schedule.finalize_schedule()
        self.assertEqual(schedule.state, "finalized")

    def test_default_active_schedule(self):
        schedule = Schedule.objects.get(academic_term="Winter 2017")
        self.assertEqual(schedule.state, "active")

    def test_return_to_active_schedule(self):
        schedule = Schedule.objects.get(academic_term="Winter 2017")
        schedule.finalize_schedule()
        self.assertEqual(schedule.state, "finalized")
        schedule.return_to_active()
        self.assertEqual(schedule.state, "active")

    def test_invalid_state(self):
        self.assertRaises(ValidationError, Schedule.create, "Winter 2019", "invalid")