class PlayerController:
    def __init__(self, master_controller):
        self.master_controller = master_controller

    def return_home(self):
        self.master_controller.show_view("home")
