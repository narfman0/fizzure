from curses import wrapper

from fizzure.main import main


def start():
    wrapper(main)


if __name__ == "__main__":
    start()  # pragma: no cover
