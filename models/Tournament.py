class Tournament:
    def __init__(self, name, location, start_date, end_date, rounds=4):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.rounds = rounds
        self.current_round = 0
        self.players = []
        self.rounds_list = []
        self.description = ""

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round_instance):
        self.rounds_list.append(round_instance)

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "rounds": self.rounds,
            "current_round": self.current_round,
            "players": [player.to_dict() for player in self.players],
            "rounds_list": [round_inst.to_dict() for round_inst in self.rounds_list],
            "description": self.description
        }
