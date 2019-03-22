import curses
import time

from fizzure import saves
from fizzure.controller import Controller
from fizzure.models import Run, Segment

COLUMN_WIDTH = 32


def main(stdscr, activator=lambda: True):
    controller = Controller()
    stdscr.clear()
    controller.run = init(stdscr)
    stdscr.clear()
    while activator():
        update(stdscr, controller)


def update(stdscr, controller):
    draw(stdscr, controller)
    stdscr.refresh()
    controller.update()
    try:
        key = stdscr.getkey()
        handle_input(stdscr, controller, key)
    except Exception:
        pass  # no input
    time.sleep(0.001)


def draw(stdscr, controller):
    y = 0
    if controller.run:
        if controller.run.game:
            declare(stdscr, "Game:", y=y)
            declare(stdscr, controller.run.game, y=y, x=COLUMN_WIDTH)
            y += 1
        if controller.run.category:
            declare(stdscr, "Category:", y=y, x=COLUMN_WIDTH)
            declare(stdscr, controller.run.category, y=y)
            y += 2
        for segment in controller.run.segments:
            declare(stdscr, segment.name, y=y)
            y += 1
    if controller.active:
        declare(stdscr, f"Time: {controller.elapsed_time:.3f}", y=y)
    else:
        declare(stdscr, "Not started!", y=y)


def handle_input(stdscr, controller, key):
    if key == "s":
        stdscr.clear()
        if controller.active:
            controller.stop()
        else:
            controller.start()
    elif key == "p":
        controller.pause()


def init(stdscr):
    stdscr.timeout(-1)
    curses.echo()
    if saves.does_default_exist():
        response = ask_question_bool(stdscr, "Use default?", y=0)
        if response:
            curses.noecho()
            stdscr.timeout(0)
            return saves.load_default()
    run = init_new_run(stdscr)
    stdscr.clear()
    response = ask_question_bool(stdscr, "Save as default?", y=0)
    if response:
        saves.save_default(run)
    curses.noecho()
    stdscr.timeout(0)
    return run


def init_new_run(stdscr):
    game = ask_question(stdscr, "What is the game name?", y=0)
    category = ask_question(stdscr, "What is the category name?", y=1)
    init_segments = ask_question_bool(stdscr, "Initialize segments?", y=2)
    y = 3
    segments = []
    if init_segments:
        segment = True
        while segment:
            segment = ask_question(stdscr, "Segment name:", y=y)
            y += 1
            segments.append(Segment(name=segment))
    return Run(segments=segments, game=game, category=category)


def declare(stdscr, message, y=0, x=0, column_width=COLUMN_WIDTH):
    stdscr.addstr(y, x, f"{message}".ljust(column_width))


def ask_question_bool(stdscr, message, y=0, x=0):
    return ask_question(stdscr, f"{message} (yN)", y=y, x=x) == "y"


def ask_question(stdscr, message, y=0, x=0, column_width=COLUMN_WIDTH):
    stdscr.addstr(y, x, f"{message}".ljust(column_width))
    return stdscr.getstr().decode("utf-8")
