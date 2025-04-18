from models.Player import Player
from models.DataManager import DataManager


class PlayerController:
    """Controller for managing player operations and data"""

    def __init__(self, master_controller):
        """Initialize player controller

        Args:
            master_controller: Main application controller
        """
        self.master_controller = master_controller
        self.data_manager = DataManager()
        self.callbacks = {
            'save_player': self.save_player,
            'load_players': self.load_players,
            'return_home': self.return_home
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view

        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def save_player(self, player_data, edit_mode=False):
        """Save a new player to the database

        Args:
            player_data (dict): Player information including:
                - last_name: Player's last name
                - first_name: Player's first name
                - birth_date: Player's birth date
                - national_id: Player's national ID
            edit_mode (bool): Whether we're editing an existing player

        Returns:
            tuple: (success: bool, message: str)
        """
        # Data validation
        if not all([player_data["last_name"],
                    player_data["first_name"],
                    player_data["birth_date"],
                    player_data["national_id"]]):
            return False, "Tous les champs sont obligatoires."

        # Validate national ID format
        national_id = player_data["national_id"].upper()
        if not (len(national_id) == 7 and
                national_id[:2].isalpha() and
                national_id[2:].isdigit()):
            return False, "L'ID national doit contenir 2 lettres suivies de 5 chiffres"

        # Check for existing player with the same ID
        players = self.load_players()
        national_id = player_data["national_id"]

        if national_id in players:
            if not edit_mode:
                # In create mode, any existing ID is an error
                return False, f"Un joueur avec l'ID {national_id} existe déjà."
            elif edit_mode and player_data.get("original_id") != national_id:
                # In edit mode, only a different existing ID is an error
                return False, f"Un joueur avec l'ID {national_id} existe déjà."
        # Validate birth date format
        try:
            day, month, year = player_data["birth_date"].split('/')
            if not (len(day) == 2 and len(month) == 2 and len(year) == 4):
                raise ValueError
            if not (1 <= int(day) <= 31
                    and 1 <= int(month) <= 12
                    and 1900 <= int(year) <= 2100):
                raise ValueError
        except ValueError:
            return False, "Format de date invalide. Utilisez JJ/MM/AAAA"

        # Create and save the new player
        player = Player(player_data["last_name"],
                        player_data["first_name"],
                        player_data["birth_date"],
                        player_data["national_id"])
        # If we're editing and the ID has changed, remove the old player entry
        if (edit_mode and
                "original_id" in player_data and
                player_data["original_id"] != player_data["national_id"]):
            self.data_manager.delete_player(player_data["original_id"])
        self.data_manager.save_player(player)

        if edit_mode:
            success_message = (f"Le joueur '{player_data['first_name']}' "
                               f"mis à jour avec succès")
        else:
            success_message = (f"Le joueur '{player_data['first_name']}' "
                               f"créé avec succès")
        return True, success_message

    def load_players(self):
        """Load all players from the database

       Returns:
            dict: Dictionary of all players, keyed by national ID
        """
        data = self.data_manager.load_data()
        return data.get("players", {})

    def return_home(self):
        """Navigate back to home view"""
        self.master_controller.show_view("home")
