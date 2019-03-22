import curses
import time

from fizzure import saves
from fizzure.controller import Controller
from fizzure.models import Run, Segment


def main(stdscr, activator=lambda: True):
    controller = Controller()
    stdscr.clear()
    controller.run = init(stdscr)
    stdscr.clear()
    while activator():
        update(stdscr, controller)


def update(stdscr, controller):
    draw_index = 0
    if controller.run:
        if controller.run.game:
            stdscr.addstr(draw_index, 0, f"Game: {controller.run.game}")
            draw_index += 1
        if controller.run.category:
            stdscr.addstr(draw_index, 0, f"Category: {controller.run.category}")
            draw_index += 1
    if controller.active:
        stdscr.addstr(draw_index, 0, f"Time: {controller.elapsed_time:.3f}")
    else:
        stdscr.addstr(draw_index, 0, f"Not started!")
    stdscr.refresh()
    controller.update()
    try:
        key = stdscr.getkey()
        handle_input(stdscr, controller, key)
    except Exception:
        pass  # no input
    time.sleep(0.001)


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
        stdscr.addstr(0, 0, "Use default? (yN)          ")
        response = stdscr.getstr()
        if response.decode("utf-8") == "y":
            curses.noecho()
            stdscr.timeout(0)
            return saves.load_default()
    run = init_new_run(stdscr)
    stdscr.clear()
    stdscr.addstr(0, 0, "Save as default? (yN)      ")
    response = stdscr.getstr()
    if response.decode("utf-8") == "y":
        saves.save_default(run)
    curses.noecho()
    stdscr.timeout(0)
    return run


def init_new_run(stdscr):
    stdscr.addstr(1, 0, "What is the game name?     ")
    game = stdscr.getstr().decode("utf-8")
    stdscr.addstr(2, 0, "What is the category name? ")
    category = stdscr.getstr().decode("utf-8")
    stdscr.addstr(3, 0, "Initialize segments? (yN)  ")
    segments = []
    response = stdscr.getstr().lower()
    draw_index = 4
    if response.decode("utf-8") == "y":
        segment = True
        while segment:
            stdscr.addstr(draw_index, 0, "Segment name:              ")
            draw_index += 1
            segment = stdscr.getstr().decode("utf-8")
            segments.append(Segment(name=segment))
    return Run(segments=segments, game=game, category=category)
