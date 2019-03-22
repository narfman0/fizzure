import os
import pickle


def does_default_exist():
    return os.path.exists(default_path())


def load_default():
    with open(default_path(), "rb") as input_file:
        return pickle.load(input_file)


def save_default(run):
    with open(default_path(), "wb") as output_file:
        pickle.dump(run, output_file)


def save_path():
    path = os.path.join(os.path.expanduser("~"), ".fizzure")
    os.makedirs(path, exist_ok=True)
    return path


def default_path():
    return os.path.join(save_path(), "default.sav")
