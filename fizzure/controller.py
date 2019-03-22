from fizzure.timer import Timer


class Controller(Timer):
    def __init__(self, run):
        super().__init__()
        self.current_segment_index = None
        self.run = run

    def next(self):
        if not self.active:
            return
        if self.run.segments and self.current_segment_index < len(self.run.segments):
            segment = self.run.segments[self.current_segment_index]
            segment.time_current = self.elapsed_time
            self.current_segment_index += 1
            if self.current_segment_index == len(self.run.segments):
                self.stop()
        else:
            self.stop()

    def start(self):
        super().start()
        self.current_segment_index = 0

    def stop(self):
        super().stop()
        self.current_segment_index = None
        self.run.stop()

    def previous_segment(self):
        if not self.active or not self.run.segments or self.current_segment_index == 0:
            return None
        return self.run.segments[self.current_segment_index - 1]

    def current_segment_duration(self):
        previous_segment = self.previous_segment()
        previous_segment_time = previous_segment.time_current if previous_segment else 0
        return self.elapsed_time - previous_segment_time

    def clear(self):
        for segment in self.run.segments:
            segment.time_pb = None
            segment.time_best = None
