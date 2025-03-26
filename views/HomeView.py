from tkinter import ttk


class HomeView(ttk.Frame):
    """Main menu view displaying navigation buttons
    for the chess tournament application"""

    def __init__(self, parent, **callbacks):
        """Initialize the home view with navigation buttons

        Args:
            parent: Parent widget containing this view
            callbacks: Dictionary containing callback functions for navigation

        Features:
            - Player management button
            - Tournament management button
            - Custom styling and cursor effects
        """
        super().__init__(parent, style='Main.TFrame')

        # Buttons
        btn_frame = ttk.Frame(self, style='Main.TFrame')
        btn_frame.pack(expand=True)

        ttk.Button(
            btn_frame,
            text="Gestion des Joueurs",
            command=callbacks.get('show_players'),
            style='Custom.TButton',
            cursor='hand2'
            ).pack(pady=10)
        ttk.Button(
            btn_frame,
            text="Gestion des Tournois",
            command=callbacks.get('show_tournaments'),
            style='Custom.TButton',
            cursor='hand2'
            ).pack(pady=10)
