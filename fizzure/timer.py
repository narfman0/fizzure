import time


class Timer:
    def __init__(self):
        self.elapsed_time = None
        self.last_time = None
        self.paused = False
        self.active = False

    def pause(self):
        if self.paused:
            self.last_time = time.time()
        self.paused = not self.paused

    def start(self):
        self.active = True
        self.paused = False
        self.elapsed_time = 0.0
        self.last_time = time.time()

    def stop(self):
        self.active = False

    def update(self):
        if self.active and not self.paused:
            new_time = time.time()
            self.elapsed_time += new_time - self.last_time
            self.last_time = new_time
