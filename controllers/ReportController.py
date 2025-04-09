class ReportController:
    """Controller for generating and displaying reports"""

    def __init__(self, master_controller):
        """Initialize report controller

        Args:
            master_controller: Main application controller
        """
        self.master_controller = master_controller
        self.data_manager = master_controller.tournament_controller.data_manager
        self.callbacks = {
            'load_all_players': self.load_all_players,
            'load_all_tournaments': self.load_all_tournaments,
            'get_tournament_details': self.get_tournament_details,
            'get_tournament_players': self.get_tournament_players,
            'get_tournament_rounds_matches': self.get_tournament_rounds_matches,
            'return_home': self.return_home
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view

        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def load_all_players(self):
        """Load all players from the database

        Returns:
            dict: Dictionary of all players
        """
        data = self.data_manager.load_data()
        return data.get("players", {})

    def load_all_tournaments(self):
        """Load all tournaments from the database

        Returns:
            dict: Dictionary of all tournaments
        """
        data = self.data_manager.load_data()
        return data.get("tournaments", {})

    def get_tournament_details(self, tournament_name):
        """Get details of a specific tournament

        Args:
            tournament_name: Name of the tournament

        Returns:
            dict: Tournament details
        """
        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        return tournaments.get(tournament_name, {})

    def get_tournament_players(self, tournament_name):
        """Get players of a specific tournament

        Args:
            tournament_name: Name of the tournament

        Returns:
            dict: Dictionary of tournament players
        """
        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        tournament = tournaments.get(tournament_name, {})

        # Get player IDs from tournament
        player_ids = tournament.get('players', [])

        # Get player details
        all_players = data.get("players", {})
        tournament_players = ({player_id: all_players.get(player_id, {})
                              for player_id in player_ids if player_id in all_players})

        return tournament_players

    def get_tournament_rounds_matches(self, tournament_name):
        """Get rounds and matches of a specific tournament

        Args:
            tournament_name: Name of the tournament

        Returns:
            list: List of rounds with matches
        """
        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        tournament = tournaments.get(tournament_name, {})

        return tournament.get('rounds_data', [])

    def return_home(self):
        """Navigate back to home view"""
        self.master_controller.show_view("home")
