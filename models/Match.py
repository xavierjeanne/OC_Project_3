class Match:
    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        self.match = [(player1, score1), (player2, score2)]

    def to_dict(self):
        return {"player1": self.match[0], "player2": self.match[1]}

    @classmethod
    def from_dict(cls, data):
        return cls(data["player1"][0],
                   data["player2"][0],
                   data["player1"][1],
                   data["player2"][1])
