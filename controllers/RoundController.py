from models.DataManager import DataManager


class RoundController:
    """Controller for managing round operations and data"""

    def __init__(self, master_controller):
        """Initialize round controller

        Args:
            master_controller: Main application controller
        """
        self.master_controller = master_controller
        self.data_manager = DataManager()
        self.callbacks = {
            'return_home': self.return_home
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view

        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def return_home(self):
        """Return to the home page"""
        self.master_controller.show_view("home")
