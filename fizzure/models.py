class Run:
    def __init__(self, segments=[], game="", category=""):
        self.version = 1
        self.segments = segments
        self.game = game
        self.category = category

    def time_best(self):
        return self.time_for_calculation("best")

    def time_current(self):
        return self.time_for_calculation("current")

    def time_pb(self):
        return self.time_for_calculation("pb")

    def time_for_calculation(self, calculation):
        dt = 0.0
        for segment in self.segments:
            segment_time = getattr(segment, f"time_{calculation}")
            if segment_time:
                dt += segment_time
        return dt

    def time_pb_complete(self):
        return self.time_complete_for_calculation("pb")

    def time_current_complete(self):
        return self.time_complete_for_calculation("current")

    def time_best_complete(self):
        return self.time_complete_for_calculation("best")

    def time_complete_for_calculation(self, calculation):
        for segment in self.segments:
            segment_time = getattr(segment, f"time_{calculation}")
            if segment_time is None:
                return False
        return True

    def stop(self):
        pb_time = self.time_pb()
        is_pb = self.time_current_complete() and (
            not self.time_pb_complete() or pb_time > self.time_current()
        )
        for segment in self.segments:
            if segment.time_current is None:
                break
            if segment.time_best is None:
                segment.time_best = segment.time_current
            else:
                segment.time_best = min(segment.time_current, segment.time_best)
            if is_pb:
                segment.time_pb = segment.time_current
            segment.time_current = None

    def upgrade(self):
        if not hasattr(self, "version"):
            self.version = 1


class Segment:
    def __init__(self, name="", time_best=None, time_pb=None, time_current=None):
        self.name = name
        self.time_best = time_best
        self.time_pb = time_pb
        self.time_current = time_current
