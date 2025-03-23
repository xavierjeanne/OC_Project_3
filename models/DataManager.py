import json
from pathlib import Path
from models.Player import Player
from models.Tournament import Tournament


class DataManager:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.save_data({"players" : {}, "tournaments" : {}})

    def load_data(self):
        with open(self.filepath, 'r', encoding="utf-8") as file:
            return json.load(file)

    def save_data(self, data):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def save_tournament(self, tournament):
        data = self.load_data()
        data["tournaments"][tournament.name] = tournament.to_dict()
        self.save_data(data)

    def load_tournament(self, name):
        data = self.load_data()
        return Tournament.from_dict(
            data["tournaments"].get(name)) if name in data["tournaments"] else None

    def save_player(self, player):
        data = self.load_data()
        data["players"][player.national_id] = player.to_dict()
        self.save_data(data)

    def load_player(self, national_id):
        data = self.load_data()
        return Player.from_dict(
            data["players"]
            .get(national_id))if national_id in data['players'] else None
