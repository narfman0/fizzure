import unittest
from unittest.mock import patch

from fizzure.controller import Controller
from fizzure.models import Run, Segment


class TestController(unittest.TestCase):
    def setUp(self):
        self.segments = [Segment(name="s1"), Segment(name="s2")]
        self.run = Run(segments=self.segments, game="smb3", category="any%")
        self.controller = Controller(self.run)

    def test_clear(self):
        self.controller.start()
        self.controller.next()
        self.controller.next()
        self.assertTrue(self.controller.run.time_pb_complete())
        self.assertIsNotNone(self.controller.run.time_pb())
        self.controller.clear()
        self.assertFalse(self.controller.run.time_pb_complete())

    def test_next(self):
        self.assertEqual(None, self.controller.current_segment_index)
        self.controller.next()
        self.assertEqual(None, self.controller.current_segment_index)
        self.controller.start()
        self.assertEqual(0, self.controller.current_segment_index)
        self.controller.next()
        self.assertEqual(1, self.controller.current_segment_index)
        self.controller.next()
        self.assertEqual(None, self.controller.current_segment_index)

    def test_next_empty_segments(self):
        self.run.segments = []
        self.controller.start()
        self.controller.next()
        self.assertEqual(None, self.controller.current_segment_index)

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

    @patch("fizzure.timer.time")
    def test_stop(self, time):
        time.time.return_value = 100.0
        self.controller.start()
        time.time.return_value = 101.0
        self.controller.update()
        self.controller.next()
        time.time.return_value = 103.0
        self.controller.update()
        self.controller.next()
