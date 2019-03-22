from fizzure.timer import Timer


class Controller(Timer):
    def __init__(self, run):
        super().__init__()
        self.current_segment_index = 0
        self.run = run

    def next(self):
        if not self.active:
            return
        if self.run.segments and self.current_segment_index <= len(self.run.segments):
            segment = self.run.segments[self.current_segment_index]
            segment.time_current = self.elapsed_time
            self.current_segment_index += 1
            if len(self.run.segments) - 1 == self.current_segment_index:
                self.stop()
        else:
            self.stop()

    def stop(self):
        super().stop()
        self.current_segment_index = 0

    def previous_segment(self):
        if not self.active or not self.run.segments or self.current_segment_index == 0:
            return None
        return self.run.segments[self.current_segment_index - 1]

    def current_segment_duration(self):
        previous_segment = self.previous_segment()
        previous_segment_time = previous_segment.time_current if previous_segment else 0
        return self.elapsed_time - previous_segment_time
