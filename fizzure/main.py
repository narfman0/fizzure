import time
from fizzure.controller import Controller


def main(stdscr):
    controller = Controller()
    stdscr.timeout(0)
    stdscr.clear()
    while True:
        if controller.active:
            stdscr.addstr(1, 0, f"elapsed_time is {controller.elapsed_time:.3f}")
        else:
            stdscr.addstr(1, 0, f"Run not started!")
        stdscr.refresh()
        controller.update()
        try:
            key = stdscr.getkey()
            if key == "s":
                stdscr.clear()
                if controller.active:
                    controller.stop()
                else:
                    controller.start()
            elif key == "p":
                controller.pause()
        except Exception:
            pass  # no input
        time.sleep(0.001)
