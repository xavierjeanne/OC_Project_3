from models.Tournament import Tournament
from models.DataManager import DataManager


class TournamentController:
    def __init__(self, master_controller):
        self.master_controller = master_controller
        self.data_manager = DataManager(
            "c:/Users/xavie/Documents/OC_Project_3/data/database.json"
            )

    def create_tournament(self, tournament_data):
        """Create new tournament"""
        try:
            tournament = Tournament(
                name=tournament_data["name"],
                location=tournament_data["location"],
                start_date=tournament_data["start_date"],
                end_date=tournament_data["end_date"],
                rounds=int(tournament_data["rounds"]),
                description=tournament_data["description"]
            )
            self.data_manager.save_tournament(tournament)
            return True, "Tournament created successfully"
        except Exception as e:
            return False, f"Error creating tournament: {str(e)}"

    def load_tournaments(self):
        """Load all tournaments"""
        data = self.data_manager.load_data()
        return data.get("tournaments", {})

    def add_players_to_tournament(self, tournament_id, player_ids):
        """Add multiple players to tournament"""
        tournament = self.data_manager.load_tournament(tournament_id)
        if not tournament:
            return False

        success_count = 0
        for player_id in player_ids:
            player = self.data_manager.load_player(player_id)
            if player and tournament.add_player(player):
                success_count += 1

        if success_count > 0:
            self.data_manager.save_tournament(tournament)
            return True
        return False

    def start_tournament(self, tournament_id):
        """Start a tournament"""
        tournament = self.data_manager.load_tournament(tournament_id)
        if tournament:
            success, message = tournament.start_tournament()
            if success:
                self.data_manager.save_tournament(tournament)
            return success, message
        return False, "Tournament not found"

    def return_home(self):
        self.master_controller.show_view("home")

    def load_available_players(self):
        """Load all available players"""
        data = self.data_manager.load_data()
        return data.get("players", {})
