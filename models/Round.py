from datetime import datetime
from models.Match import Match


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None

    def add_match(self, match):
        self.matches.append(match)

    def end_round(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data):
        round_instance = cls(data["name"])
        round_instance.matches = [Match.from_dict(match) for match in data["matches"]]
        round_instance.start_time = data["start_time"]
        round_instance.end_time = data["end_time"]
        return round_instance
