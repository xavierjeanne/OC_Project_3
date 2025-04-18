import json
from pathlib import Path
from models.Player import Player
from models.Tournament import Tournament


class DataManager:
    """Manages data persistence for the chess tournament application"""

    def __init__(self, filepath="data/database.json"):
        """Initialize the data manager with a file path

        Args:
            filepath (str): Path to the JSON database file,
            defaults to data/database.json
        """
        self.filepath = Path(filepath)
        # Ensure the file exists, create if not
        self.filepath.parent.mkdir(parents=True,
                                   exist_ok=True)
        if not self.filepath.exists():
            self.save_data({"players": {}, "tournaments": {}})

    def load_data(self):
        """Load all data from the JSON file

        Returns:
            dict: Dictionary containing all application data
        """
        with open(self.filepath,
                  'r',
                  encoding="utf-8") as file:
            return json.load(file)

    def save_data(self, data):
        """Save data to the JSON file

        Args:
            data (dict): Data to be saved
        """
        with open(self.filepath,
                  "w",
                  encoding="utf-8") as file:
            json.dump(data,
                      file,
                      indent=4)

    def save_tournament(self, tournament):
        """Save a tournament to the database

        Args:
            tournament: Tournament object to save
        """
        data = self.load_data()

        # Initialize tournaments dictionary if it doesn't exist
        if "tournaments" not in data:
            data["tournaments"] = {}

        data["tournaments"][tournament.name] = tournament.to_dict()
        self.save_data(data)

    def load_tournament(self, name):
        """Load a tournament from the database

        Args:
            name (str): Name of the tournament to load

        Returns:
            Tournament: Tournament object if found, None otherwise
        """
        data = self.load_data()
        return Tournament.from_dict(
            data["tournaments"].get(name)) if name in data["tournaments"] else None

    def save_player(self, player):
        """Save a player to the database

        Args:
            player: Player object to save
        """
        data = self.load_data()

        # Initialize the players dictionary if it doesn't exist
        if "players" not in data:
            data["players"] = {}

        data["players"][player.national_id] = player.to_dict()
        self.save_data(data)

    def load_player(self, national_id):
        """Load a player from the database

        Args:
            national_id (str): National ID of the player to load

        Returns:
            Player: Player object if found, None otherwise
        """
        data = self.load_data()
        return Player.from_dict(
            data["players"]
            .get(national_id)) if national_id in data['players'] else None

    def delete_player(self, national_id):
        """Delete a player from the database

        Args:
            national_id (str): National ID of the player to delete
        Returns:
            bool: True if player was deleted, False if not found
        """
        data = self.load_data()

        if "players" in data and national_id in data["players"]:
            del data["players"][national_id]
            self.save_data(data)
            return True
        return False
