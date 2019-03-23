import unittest
from unittest.mock import MagicMock, patch

from fizzure import main


class TestMain(unittest.TestCase):
    @patch("fizzure.main.init")
    @patch("fizzure.main.update")
    def test_main(self, update, init):
        def activator():
            self.hits += 1
            return self.hits < 2

        stdscr = MagicMock()
        self.hits = 0
        main.main(stdscr, activator)

    @patch("fizzure.main.ask_question_bool")
    @patch("fizzure.main.curses")
    @patch("fizzure.main.init_new_run")
    @patch("fizzure.main.saves")
    def test_init(self, saves, init_new_run, curses, ask_question_bool):
        run = MagicMock(game="game1")
        ask_question_bool.side_effect = [False, True]
        init_new_run.return_value = run
        stdscr = MagicMock()
        result_run = main.init(stdscr)
        self.assertEqual(run.game, result_run.game)

    @patch("fizzure.main.handle_input")
    def test_update(self, handle_input):
        def no_input():
            raise Exception("No input!")

        stdscr = MagicMock()
        controller = MagicMock(elapsed_time=1.0)
        main.update(stdscr, controller)
        controller.active = False
        main.update(stdscr, controller)
        handle_input.side_effect = no_input
        main.update(stdscr, controller)

    def test_handle_input(self):
        stdscr = MagicMock()
        controller = MagicMock(active=False)
        main.handle_input(stdscr, controller, "s")
        self.assertTrue(controller.start.called)
        controller.active = True
        main.handle_input(stdscr, controller, "p")
        self.assertTrue(controller.pause.called)
        main.handle_input(stdscr, controller, "s")
        self.assertTrue(controller.stop.called)
