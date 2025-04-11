from datetime import datetime


class Tournament:
    """Represents a chess tournament with players, rounds, and matches"""

    def __init__(self, name, location, start_date, end_date, rounds, description):
        """Initialize a new tournament

        Args:
            name (str): Tournament name
            location (str): Tournament location
            start_date (str): Start date in DD/MM/YYYY format
            end_date (str): End date in DD/MM/YYYY format
            rounds (int): Number of rounds
            description (str): Tournament description
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.rounds = rounds
        self.description = description
        self.players = []
        self.current_round = 0
        self.rounds_data = []
        self.status = "Non démarré"  # Add default status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_player(self, player):
        """Add a player to the tournament if not already registered

        Args:
            player (Player): Player object to add

        Returns:
            bool: True if player was added, False if already registered
        """
        if player not in self.players:
            self.players.append(player)
            return True
        return False

    def to_dict(self):
        """Convert tournament data to dictionary format for storage

        Returns:
            dict: Tournament data including players, matches, and history
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "rounds": self.rounds,
            "current_round": self.current_round,
            "description": self.description,
            "players": [player.national_id for player in self.players],
            "created_at": self.created_at,
            "status": self.status  # Add status to the dictionary
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Tournament instance from dictionary data

        Args:
            data (dict): Dictionary containing tournament data

        Returns:
            Tournament: New Tournament instance with loaded data
        """
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data["rounds"],
            data["current_round"],
            data["description"],
            data['status'],
        )
        tournament.created_at = data["created_at"]
        return tournament
