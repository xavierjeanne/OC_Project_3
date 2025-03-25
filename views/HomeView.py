from tkinter import ttk


class HomeView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Main.TFrame')
        self.controller = controller

        # Buttons
        btn_frame = ttk.Frame(self, style='Main.TFrame')
        btn_frame.pack(expand=True)

        ttk.Button(
            btn_frame,
            text="Gestion des Joueurs",
            command=self.controller.show_players,
            style='Custom.TButton',
            cursor='hand2'
            ).pack(pady=10)
        ttk.Button(
            btn_frame,
            text="Gestion des Tournois",
            command=self.controller.show_tournaments,
            style='Custom.TButton',
            cursor='hand2'
            ).pack(pady=10)
