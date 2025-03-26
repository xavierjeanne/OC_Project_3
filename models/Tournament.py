from datetime import datetime


class Tournament:
    """Represents a chess tournament with players, rounds, and matches"""

    def __init__(self, name, location, start_date, end_date, rounds=4,
                 current_round=1, description=""):
        """Initialize a tournament with its basic information

        Args:
            name (str): Tournament name
            location (str): Tournament location
            start_date (str): Start date of tournament
            end_date (str): End date of tournament
            rounds (int): Number of rounds (default: 4)
            current_round (int): Current round number (default: 1)
            description (str): Tournament description (default: empty)
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.rounds = rounds
        self.current_round = current_round
        self.description = description
        self.players = []
        self.matches = []
        self.rounds_history = []
        self.status = "Not Started"  # Not Started, In Progress, Completed
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

    def start_tournament(self):
        """Start the tournament if conditions are met

        Returns:
            tuple: (success: bool, message: str)
        """
        if len(self.players) < 2:
            return False, "Not enough players"
        if len(self.players) % 2 != 0:
            return False, "Need even number of players"
        self.status = "In Progress"
        return True, "Tournament started"

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
            "matches": self.matches,
            "rounds_history": self.rounds_history,
            "status": self.status,
            "created_at": self.created_at
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
            data["description"]
        )
        tournament.matches = data["matches"]
        tournament.rounds_history = data["rounds_history"]
        tournament.status = data["status"]
        tournament.created_at = data["created_at"]
        return tournament
