import os
import pickle

DEFAULT_NAME = "default.sav"


def exists(name=DEFAULT_NAME):
    return os.path.exists(path(name))


def load(name=DEFAULT_NAME):
    with open(path(name), "rb") as input_file:
        run = pickle.load(input_file)
        run.upgrade()
        return run


def save(run, name=DEFAULT_NAME):
    with open(path(name), "wb") as output_file:
        pickle.dump(run, output_file)


def path(name=DEFAULT_NAME):
    directory = os.path.join(os.path.expanduser("~"), ".fizzure")
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, name)
