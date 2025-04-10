from views.BaseView import BaseView
from controllers.HomeController import HomeController
from controllers.PlayerController import PlayerController
from controllers.TournamentController import TournamentController
from controllers.RoundController import RoundController
from views.RoundView import RoundView
from views.HomeView import HomeView
from views.PlayerView import PlayerView
from views.TournamentView import TournamentView
from controllers.ReportController import ReportController
from views.ReportView import ReportView


class MainController:
    """Main application controller managing views and sub-controllers"""

    def __init__(self, root):
        """Initialize the main application controller

        Args:
            root: The root Tkinter window

        Features:
            - Sets up main window properties
            - Initializes base view
            - Creates and manages sub-controllers
            - Manages view navigation
        """
        self.root = root
        self.root.title("Gestion de tournois d'échecs")
        self.root.geometry("1024x768")
        self.base_view = BaseView(root)

        # Initialize controllers
        self.home_controller = HomeController(self)
        self.player_controller = PlayerController(self)
        self.tournament_controller = TournamentController(self)
        # Initialize round controller after tournament controller
        self.round_controller = RoundController(self)
        self.report_controller = ReportController(self)

        # Make sure the round controller has access to the tournament controller
        self.round_controller.tournament_controller = self.tournament_controller

        # Initialize views
        self.views = {}
        self.views["home"] = HomeView(
            self.base_view.content_container,
            **self.home_controller.get_callbacks()
        )
        self.views["players"] = PlayerView(
            self.base_view.content_container,
            **self.player_controller.get_callbacks()
        )
        self.views["tournaments"] = TournamentView(
            self.base_view.content_container,
            **self.tournament_controller.get_callbacks()
        )
        self.views["rounds"] = RoundView(
            self.base_view.content_container,
            **self.round_controller.get_callbacks()
        )
        self.views["reports"] = ReportView(
            self.base_view.content_container,
            **self.report_controller.get_callbacks()
        )
        # Configure all views
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
        # Show home view by default
        self.show_view("home")

    def show_view(self, view_name):
        """Switch to the specified view

        Args:
            view_name (str): Name of the view to display
            ('home', 'players', or 'tournaments')
        """
        # If switching to rounds view, make sure tournament data is passed
        if view_name == "rounds" :
            self.views["rounds"].show()

        self.views[view_name].tkraise()
