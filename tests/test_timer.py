import unittest
from unittest.mock import patch

from fizzure.timer import Timer


class TestTimer(unittest.TestCase):
    @patch("fizzure.timer.time")
    def test_pause(self, time):
        time.time.return_value = 100.0
        timer = Timer()
        timer.start()
        self.assertEqual(0.0, timer.elapsed_time)
        time.time.return_value = 101.0
        timer.pause()
        timer.update()
        self.assertEqual(0.0, timer.elapsed_time)
        timer.pause()
        time.time.return_value = 101.5
        timer.update()
        self.assertEqual(0.5, timer.elapsed_time)

    @patch("fizzure.timer.time")
    def test_stop(self, time):
        time.time.return_value = 100.0
        timer = Timer()
        timer.start()
        self.assertEqual(0.0, timer.elapsed_time)
        time.time.return_value = 101.0
        timer.stop()
        timer.update()
        self.assertEqual(0.0, timer.elapsed_time)

    @patch("fizzure.timer.time")
    def test_update(self, time):
        time.time.return_value = 100.0
        timer = Timer()
        timer.start()
        self.assertEqual(0.0, timer.elapsed_time)
        time.time.return_value = 101.0
        timer.update()
        self.assertEqual(1.0, timer.elapsed_time)
        time.time.return_value = 102.5
        timer.update()
        self.assertEqual(2.5, timer.elapsed_time)
