class Run:
    def __init__(self, segments=[], game="", category=""):
        self.segments = segments
        self.game = game
        self.category = category


class Segment:
    def __init__(self, name=""):
        self.name = name
        self.duration = 0
