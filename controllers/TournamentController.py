from models.Tournament import Tournament
from models.DataManager import DataManager


class TournamentController:
    """Controller for managing tournament operations and data"""

    def __init__(self, master_controller):
        """Initialize tournament controller

        Args:
            master_controller: Main application controller
        """
        self.master_controller = master_controller
        self.data_manager = DataManager()
        self.callbacks = {
            'save_tournament': self.save_tournament,
            'load_tournaments': self.load_tournaments,
            'load_available_players': self.load_available_players,
            'add_players_to_tournament': self.add_players_to_tournament,
            'return_home': self.return_home,
            'open_round_page': self.open_round_page,
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view

        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def save_tournament(self, tournament_data,  edit_mode=False):
        """Create and save a new tournament

        Args:
            tournament_data (dict): Tournament information including:
                - name: Tournament name
                - location: Tournament location
                - start_date: Start date
                - end_date: End date
                - rounds: Number of rounds
                - description: Tournament description

        Returns:
            tuple: (success: bool, message: str)
        """

        # Data validation
        if not all([tournament_data["name"],
                    tournament_data["location"],
                    tournament_data["start_date"],
                    tournament_data["end_date"],
                    tournament_data["rounds"],
                    tournament_data["description"]]):
            return False, "Tous les champs sont obligatoires."

        tournaments = self.load_tournaments()
        if tournament_data["name"] in tournaments:
            if not edit_mode:
                # In create mode, any existing name is an error
                message = (f"Un tournoi avec le nom {tournament_data['name']} "
                           f"existe déjà.")
                return False, message
            elif edit_mode and (tournament_data.get("original_name")
                                != tournament_data["name"]):
                # In edit mode, only a different existing name is an error
                message = (f"Un tournoi avec le nom {tournament_data['name']} "
                           f"existe déjà.")
                return False, message

        try:
            start_day, start_month, start_year = tournament_data["start_date"].split(
                '/')
            if not (len(start_day) == 2
                    and len(start_month) == 2
                    and len(start_year) == 4):
                raise ValueError
            if not (1 <= int(start_day) <= 31
                    and 1 <= int(start_month) <= 12
                    and 1900 <= int(start_year) <= 2100):
                raise ValueError
            start_date_int = int(start_year + start_month + start_day)
        except ValueError:
            return False, "Format de date invalide . Utilisez JJ/MM/AAAA"
        try:
            end_day, end_month, end_year = tournament_data["end_date"].split('/')
            if not (len(end_day) == 2 and len(end_month) == 2 and len(end_year) == 4):
                raise ValueError
            if not (1 <= int(end_day) <= 31
                    and 1 <= int(end_month) <= 12
                    and 1900 <= int(end_year) <= 2100):
                raise ValueError
            end_date_int = int(end_year + end_month + end_day)
        except ValueError:
            return False, "Format de date invalide. Utilisez JJ/MM/AAAA"

        if end_date_int < start_date_int:
            return False, "La date de fin doit être postérieure à la date de début."

        tournament = Tournament(
                name=tournament_data["name"],
                location=tournament_data["location"],
                start_date=tournament_data["start_date"],
                end_date=tournament_data["end_date"],
                rounds=int(tournament_data["rounds"]),
                description=tournament_data["description"]
            )
        self.data_manager.save_tournament(tournament)
        if edit_mode:
            success_message = (f"Tournoi '{tournament_data['name']}'"
                               f"mis à jour avec succès")
        else:
            success_message = f"Tournoi '{tournament_data['name']}' créé avec succès"
        return True, success_message

    def load_tournaments(self):
        """Load all tournaments from the database

        Returns:
            dict: Dictionary of all tournaments, keyed by name
        """
        data = self.data_manager.load_data()
        return data.get("tournaments", {})

    def load_available_players(self):
        """Load all available players for tournament selection

        Returns:
            dict: Dictionary of all players, keyed by national ID
        """
        data = self.data_manager.load_data()
        return data.get("players", {})

    def add_players_to_tournament(self, name, player_ids):
        """Add multiple players to a tournament

        Args:
            name: Name of the tournament
            player_ids: List of player IDs to add

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Load the complete data structure
            data = self.data_manager.load_data()
            tournaments = data.get("tournaments", {})

            if name not in tournaments:
                return False, "Tournoi non trouvé"

            tournament = tournaments[name]
            # Check if there's at least one player

            player_count = len(player_ids)

            if player_count % 2 != 0:
                return False, "Veuillez sélectionner un nombre de joueur pair"
            # Update the player list
            tournament['players'] = list(player_ids)

            message = f"Liste des joueurs mise à jour ({player_count} joueurs)"

            # Save the complete data structure
            data["tournaments"] = tournaments
            self.data_manager.save_data(data)

            return True, message
        except Exception as e:
            return False, f"Erreur lors de l'ajout des joueurs: {str(e)}"

    def return_home(self):
        """Navigate back to home view"""
        self.master_controller.show_view("home")

    def open_round_page(self, tournament_name):
        """Open the round management page for the selected tournament
        Args:
            tournament_name: Name of the tournament to manage rounds for
        """
        # Get the tournament data
        tournaments = self.load_tournaments()
        tournament_data = tournaments.get(tournament_name)

        if not tournament_data:
            return False, "Tournoi non trouvé"

        # Check if the tournament has enough players
        if len(tournament_data.get('players', [])) < 2:
            return False, "Le tournoi doit avoir au moins 2 joueurs"

        # Store the tournament name in the controller for access by the rounds view
        self.current_tournament = tournament_name

        # Navigate to the round page - only pass the view name
        self.master_controller.show_view("rounds")
        return True, f"Affichage des tours pour {tournament_name}"
