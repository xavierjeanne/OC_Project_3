class Match:
    """Represents a chess match between two players with their respective scores"""

    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        """Initialize a match with two players and their scores

        Args:
            player1: First player object
            player2: Second player object
            score1 (float): Score of first player (default: 0.0)
            score2 (float): Score of second player (default: 0.0)
        """
        self.match = [(player1, score1),
                      (player2, score2)]

    def to_dict(self):
        """Convert match data to dictionary format for storage

        Returns:
            dict: Match data in dictionary format
        """
        return {"player1": self.match[0],
                "player2": self.match[1]}

    @classmethod
    def from_dict(cls, data):
        """Create a Match instance from dictionary data

        Args:
            data (dict): Dictionary containing match data

        Returns:
            Match: New Match instance with loaded data
        """
        return cls(data["player1"][0],
                   data["player2"][0],
                   data["player1"][1],
                   data["player2"][1])
