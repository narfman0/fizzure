class Run:
    def __init__(self, segments=[], game="", category=""):
        self.version = 1
        self.segments = segments
        self.game = game
        self.category = category

    def upgrade(self):
        if not hasattr(self, "version"):
            self.version = 1
            for segment in self.segments:
                segment.time_best = None
                segment.time_pb = None
                segment.time_current = None


class Segment:
    def __init__(self, name=""):
        self.name = name
        self.time_best = None
        self.time_pb = None
        self.time_current = None
