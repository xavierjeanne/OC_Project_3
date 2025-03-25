from tkinter import ttk
from models.DataManager import DataManager


class TournamentView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Main.TFrame')
        self.controller = controller

        # Initialisation du gestionnaire de données
        self.data_manager = DataManager(
            "c:/Users/xavie/Documents/OC_Project_3/data/database.json"
            )

        ttk.Button(self,
                   text="Retour à l'accueil",
                   command=self.controller.return_home,
                   cursor='hand2',
                   style='Custom.TButton').grid(row=0, column=0, pady=10)
        # Création des onglets
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Onglet création de tournoi
        self.create_tournament_frame = ttk.Frame(self.notebook,
                                                 style='Custom.TNotebook.Tab')
        self.notebook.add(self.create_tournament_frame, text="Nouveau Tournoi")
        self._setup_create_tournament_tab()

        # Onglet liste des tournois
        self.list_tournaments_frame = ttk.Frame(self.notebook,
                                                style='Custom.TNotebook.Tab')
        self.notebook.add(self.list_tournaments_frame, text="Liste des Tournois")
        self._setup_list_tournaments_tab()

        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _setup_create_tournament_tab(self):
        # Implémentez la création de tournoi ici
        pass

    def _setup_list_tournaments_tab(self):
        # Implémentez la liste des tournois ici
        pass
