from models.Player import Player
from models.DataManager import DataManager


class PlayerController:
    def __init__(self, master_controller):
        self.master_controller = master_controller
        self.data_manager = DataManager(
            "c:/Users/xavie/Documents/OC_Project_3/data/database.json"
            )

    def save_player(self, player_data):
        """Handle player saving logic"""
        # Validation des données
        if not all([player_data["last_name"], player_data["first_name"],
                    player_data["birth_date"], player_data["national_id"]]):
            return False, "Tous les champs sont obligatoires."

        # Vérification si le joueur existe déjà
        existing_player = self.data_manager.load_player(player_data["national_id"])
        if existing_player:
            return False,
        f"Un joueur avec l'ID {player_data['national_id']} existe déjà."

        # Création et sauvegarde du joueur
        player = Player(player_data["last_name"], player_data["first_name"],
                        player_data["birth_date"], player_data["national_id"])
        self.data_manager.save_player(player)
        message = (f"Le joueur {player_data['first_name']} "
                   f"{player_data['last_name']} a été enregistré.")
        return True, message

    def load_players(self):
        """Load all players"""
        data = self.data_manager.load_data()
        return data.get("players", {})

    def return_home(self):
        self.master_controller.show_view("home")
