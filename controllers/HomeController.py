class HomeController:
    """Controller for managing home view navigation"""

    def __init__(self, master_controller):
        """Initialize home controller

        Args:
            master_controller: Main application controller for view management
        """
        self.master_controller = master_controller
        self.callbacks = {
            'show_players': self.show_players,
            'show_tournaments': self.show_tournaments,
            'show_reports': self.show_reports
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view

        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def show_players(self):
        """Navigate to players management view"""
        self.master_controller.show_view("players")

    def show_tournaments(self):
        """Navigate to tournaments management view"""
        self.master_controller.show_view("tournaments")

    def show_reports(self):
        """Navigate to reports management view"""
        self.master_controller.show_view("reports")
