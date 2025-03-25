from datetime import datetime


class Tournament:
    def __init__(self,
                 name,
                 location,
                 start_date,
                 end_date,
                 rounds=4,
                 current_round=1,
                 description=""):
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
        """Add a player to the tournament"""
        if player not in self.players:
            self.players.append(player)
            return True
        return False

    def start_tournament(self):
        """Start the tournament"""
        if len(self.players) < 2:
            return False, "Not enough players"
        if len(self.players) % 2 != 0:
            return False, "Need even number of players"
        self.status = "In Progress"
        return True, "Tournament started"

    def record_match(self, player1, player2, result):
        """Record a match result"""
        match = {
            "round": self.current_round,
            "player1": player1,
            "player2": player2,
            "result": result,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.matches.append(match)

    def end_round(self):
        """End current round and prepare next"""
        if self.current_round < self.rounds:
            self.rounds_history.append({
                "round": self.current_round,
                "matches": self.matches.copy()
            })
            self.current_round += 1
            return True
        self.status = "Completed"
        return False

    def to_dict(self):
        """Convert tournament to dictionary for storage"""
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
        """Create tournament instance from dictionary"""
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
