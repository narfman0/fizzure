import unittest

from fizzure import saves
from fizzure.models import Run, Segment


class TestSaves(unittest.TestCase):
    def test_save_load_exists(self):
        name = "test"
        category = "category"
        segments = [Segment("s1"), Segment("s2")]
        run = Run(segments=segments, game=name, category=category)
        saves.save(run, name=name)
        self.assertTrue(saves.exists(name))
        run_loaded = saves.load(name)
        self.assertEqual(name, run_loaded.game)
        self.assertEqual(category, run_loaded.category)
        self.assertEqual(segments, run.segments)
