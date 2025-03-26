from datetime import datetime
from models.Match import Match


class Round:
    """Represents a round in a chess tournament containing multiple matches"""

    def __init__(self, name):
        """Initialize a round with a name and start time

        Args:
            name (str): Name of the round (e.g., 'Round 1')
        """
        self.name = name
        self.matches = []
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None

    def add_match(self, match):
        """Add a match to the round

        Args:
            match (Match): Match object to add to the round
        """
        self.matches.append(match)

    def end_round(self):
        """End the round and record the end time"""
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Convert round data to dictionary format for storage

        Returns:
            dict: Round data including matches, start and end times
        """
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Round instance from dictionary data

        Args:
            data (dict): Dictionary containing round data

        Returns:
            Round: New Round instance with loaded data
        """
        round_instance = cls(data["name"])
        round_instance.matches = [Match.from_dict(match) for match in data["matches"]]
        round_instance.start_time = data["start_time"]
        round_instance.end_time = data["end_time"]
        return round_instance
