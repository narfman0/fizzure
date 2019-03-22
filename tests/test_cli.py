import unittest
from unittest.mock import patch

from fizzure import cli


class TestCLI(unittest.TestCase):
    @patch("fizzure.cli.main")
    @patch("fizzure.cli.wrapper")
    def test_start(self, main, wrapper):
        cli.start()
