import unittest
from unittest.mock import patch

from fizzure.controller import Controller


class TestController(unittest.TestCase):
    @patch("fizzure.controller.time")
    def test_controller_update(self, time):
        time.time.return_value = 100.0
        controller = Controller()
        controller.start()
        self.assertEqual(0.0, controller.elapsed_time)
        time.time.return_value = 101.0
        controller.update()
        self.assertEqual(1.0, controller.elapsed_time)
        time.time.return_value = 102.5
        controller.update()
        self.assertEqual(2.5, controller.elapsed_time)
