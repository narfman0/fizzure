import curses
import math
import sys
import time

from fizzure import saves
from fizzure.controller import Controller
from fizzure.models import Run, Segment

COLUMN_WIDTH = 32
COLUMN_WIDTH_SM = 14


def main(stdscr, activator=lambda: True):
    stdscr.clear()
    run = init(stdscr)
    controller = Controller(run)
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
            declare(stdscr, controller.run.game, y=y, x=COLUMN_WIDTH_SM)
            y += 1
        if controller.run.category:
            declare(stdscr, "Category:", y=y)
            declare(stdscr, controller.run.category, y=y, x=COLUMN_WIDTH_SM)
            y += 1
        if controller.run.segments:
            declare(stdscr, "Name", y=y)
            declare(stdscr, "Best", y=y, x=COLUMN_WIDTH_SM)
            declare(stdscr, "PB", y=y, x=2 * COLUMN_WIDTH_SM)
            declare(stdscr, "Current", y=y, x=3 * COLUMN_WIDTH_SM)
            y += 1
        for index, segment in enumerate(controller.run.segments):
            declare(stdscr, segment.name, y=y)
            if segment.time_best:
                message = pretty_time(segment.time_best)
                declare(stdscr, message, y=y, x=COLUMN_WIDTH_SM)
            if segment.time_pb:
                message = pretty_time(segment.time_pb)
                declare(stdscr, message, y=y, x=2 * COLUMN_WIDTH_SM)
            if segment.time_current:
                message = pretty_time(segment.time_current)
                declare(stdscr, message, y=y, x=3 * COLUMN_WIDTH_SM)
            if index == controller.current_segment_index:
                declare(stdscr, "<", y=y, x=4 * COLUMN_WIDTH_SM)
            y += 1
    if controller.active:
        declare(stdscr, "Time:", y=y)
        message = pretty_time(controller.elapsed_time)
        declare(stdscr, message, y=y, x=3 * COLUMN_WIDTH_SM)
    else:
        declare(stdscr, "Not started!", y=y, column_width=0)


def handle_input(stdscr, controller, key):
    if key == "s":
        stdscr.clear()
        if controller.active:
            controller.stop()
        else:
            controller.start()
    elif key == "p":
        controller.pause()
    elif key == "n":
        controller.next()
        if not controller.active:
            stdscr.clear()
    elif key == "c":
        controller.clear()
    elif key == "q":
        saves.save(controller.run)
        sys.exit(0)


def init(stdscr):
    stdscr.timeout(-1)
    curses.echo()
    if saves.exists():
        response = ask_question_bool(stdscr, "Use default?", y=0)
        if response:
            curses.noecho()
            stdscr.timeout(0)
            return saves.load()
    run = init_new_run(stdscr)
    stdscr.clear()
    response = ask_question_bool(stdscr, "Save as default?", y=0)
    if response:
        saves.save(run)
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
            if segment:
                segments.append(Segment(name=segment))
    return Run(segments=segments, game=game, category=category)


def pretty_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    frac, whole = math.modf(seconds)
    ms = frac * 1000
    return "%d:%02d:%02d.%02d" % (h, m, s, ms)


def declare(stdscr, message, y=0, x=0, column_width=COLUMN_WIDTH):
    stdscr.addstr(y, x, f"{message}".ljust(column_width))


def ask_question_bool(stdscr, message, **kwargs):
    return ask_question(stdscr, f"{message} (yN)", **kwargs) == "y"


def ask_question(stdscr, message, **kwargs):
    declare(stdscr, message, **kwargs)
    return stdscr.getstr().decode("utf-8")
