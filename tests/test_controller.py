import unittest
from unittest.mock import patch

from fizzure.controller import Controller
from fizzure.models import Run, Segment


class TestController(unittest.TestCase):
    def setUp(self):
        self.segments = [Segment(name="s1"), Segment(name="s2")]
        self.run = Run(segments=self.segments, game="smb3", category="any%")
        self.controller = Controller(self.run)

    def test_next(self):
        self.assertEqual(0, self.controller.current_segment_index)
        self.controller.next()
        self.assertEqual(0, self.controller.current_segment_index)
        self.controller.start()
        self.assertEqual(0, self.controller.current_segment_index)
        self.controller.next()
        self.assertEqual(1, self.controller.current_segment_index)
        self.controller.next()

    def test_previous_segment(self):
        self.assertIsNone(self.controller.previous_segment())
        self.controller.next()
        self.assertIsNone(self.controller.previous_segment())
        self.controller.start()
        self.assertIsNone(self.controller.previous_segment())
        self.controller.next()
        self.assertEqual("s1", self.controller.previous_segment().name)

    @patch("fizzure.timer.time")
    def test_current_segment_duration(self, time):
        time.time.return_value = 100.0
        self.controller.start()
        self.assertEqual(0.0, self.controller.current_segment_duration())
        time.time.return_value = 101.0
        self.controller.update()
        self.assertEqual(1.0, self.controller.current_segment_duration())
        self.controller.next()
        self.assertEqual(0.0, self.controller.current_segment_duration())
        time.time.return_value = 103.0
        self.controller.update()
        self.assertEqual(2.0, self.controller.current_segment_duration())
