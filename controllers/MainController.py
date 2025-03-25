from views.BaseView import BaseView
from controllers.HomeController import HomeController
from controllers.PlayerController import PlayerController
from controllers.TournamentController import TournamentController
from views.HomeView import HomeView
from views.PlayerView import PlayerView
from views.TournamentView import TournamentView


class MainController:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Tournament Manager")
        self.root.geometry("1024x768")
        self.base_view = BaseView(root)

        # Initialize controllers
        self.home_controller = HomeController(self)
        self.player_controller = PlayerController(self)
        self.tournament_controller = TournamentController(self)

        # Initialize views
        self.views = {}
        self.views["home"] = HomeView(self.base_view.content_container,
                                      self.home_controller)
        self.views["players"] = PlayerView(self.base_view.content_container,
                                           self.player_controller)
        self.views["tournaments"] = TournamentView(self.base_view.content_container,
                                                   self.tournament_controller)

        # Configure all views
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
        # Show home view by default
        self.show_view("home")

    def show_view(self, view_name):
        """Switch to the specified view"""
        self.views[view_name].tkraise()
