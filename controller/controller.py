from models.DataManager import DataManager


class Controller:
    def run(self):
        db = DataManager("data/database.json")
        loaded_player = db.load_player("NO12346")
        if loaded_player:
            print(f"Joueur :{loaded_player.first_name} {loaded_player.last_name}")
        else:
            print("Joueur non trouvé !")
