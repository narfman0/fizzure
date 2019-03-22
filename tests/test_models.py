import unittest

from fizzure.models import Run, Segment


class TestModels(unittest.TestCase):
    def test_upgrade(self):
        run = Run()
        del run.version
        run.upgrade()

    def test_time_current(self):
        segments = [Segment(name="s1"), Segment(name="s2")]
        run = Run(segments=segments, game="smb3", category="any%")
        run.time_current()
        segments[0].time_current = 1
        self.assertEqual(1, run.time_current())
