class HomeController:
    def __init__(self, master_controller):
        self.master_controller = master_controller

    def show_players(self):
        self.master_controller.show_view("players")

    def show_tournaments(self):
        self.master_controller.show_view("tournaments")
