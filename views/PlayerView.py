import tkinter as tk
from tkinter import ttk, messagebox
from models.Player import Player
from models.DataManager import DataManager


class PlayerView(ttk.Frame):
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

        # Onglet d'ajout de joueur
        self.add_player_frame = ttk.Frame(self.notebook, style='Custom.TNotebook.Tab')
        self.notebook.add(self.add_player_frame, text="Ajouter un joueur")
        self._setup_add_player_tab()

        # Onglet de liste des joueurs
        self.list_players_frame = ttk.Frame(self.notebook, style='Custom.TNotebook.Tab')
        self.notebook.add(self.list_players_frame, text="Liste des joueurs")
        self._setup_list_players_tab()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _setup_add_player_tab(self):
        """Configure l'onglet d'ajout de joueur"""
        # Configuration du layout
        for i in range(5):
            self.add_player_frame.grid_rowconfigure(i, weight=1)
        self.add_player_frame.grid_columnconfigure(0, weight=1)
        self.add_player_frame.grid_columnconfigure(1, weight=2)

        # Champs de saisie
        fields = [
            ("Nom:", "last_name"),
            ("Prénom:", "first_name"),
            ("Date de naissance (JJ/MM/AAAA):", "birth_date"),
            ("Identifiant national:", "national_id")
        ]

        self.entries = {}
        for idx, (label_text, field_name) in enumerate(fields):
            # Label
            label = ttk.Label(self.add_player_frame, text=label_text)
            label.grid(row=idx, column=0, sticky='e', padx=10, pady=10)

            # Champ de saisie
            entry = ttk.Entry(self.add_player_frame, width=30)
            entry.grid(row=idx, column=1, sticky='w', padx=10, pady=10)
            self.entries[field_name] = entry

        # Bouton de validation
        save_btn = ttk.Button(
            self.add_player_frame,
            text="Enregistrer",
            command=self.save_player,
        )
        save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def _setup_list_players_tab(self):
        """Configure l'onglet de liste des joueurs"""
        # Configuration du layout
        self.list_players_frame.grid_rowconfigure(0, weight=1)
        self.list_players_frame.grid_columnconfigure(0, weight=1)

        # Création du tableau
        columns = ("national_id", "last_name", "first_name", "birth_date")
        self.players_table = ttk.Treeview(self.list_players_frame,
                                          columns=columns,
                                          show='headings')

        # Configuration des en-têtes
        self.players_table.heading("national_id", text="ID National")
        self.players_table.heading("last_name", text="Nom")
        self.players_table.heading("first_name", text="Prénom")
        self.players_table.heading("birth_date", text="Date de naissance")

        # Configuration des colonnes
        self.players_table.column("national_id", width=100)
        self.players_table.column("last_name", width=150)
        self.players_table.column("first_name", width=150)
        self.players_table.column("birth_date", width=150)

        # Ajout d'une barre de défilement
        scrollbar = ttk.Scrollbar(self.list_players_frame,
                                  orient=tk.VERTICAL,
                                  command=self.players_table.yview)
        self.players_table.configure(yscroll=scrollbar.set)

        # Placement des éléments
        self.players_table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Chargement des joueurs
        self.load_players()

    def save_player(self):
        """Enregistre un nouveau joueur"""
        # Récupération des données du formulaire
        last_name = self.entries["last_name"].get().strip()
        first_name = self.entries["first_name"].get().strip()
        birth_date = self.entries["birth_date"].get().strip()
        national_id = self.entries["national_id"].get().strip()

        # Validation des données
        if not all([last_name, first_name, birth_date, national_id]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        # Vérification si le joueur existe déjà
        existing_player = self.data_manager.load_player(national_id)
        if existing_player:
            messagebox.showerror(
                "Erreur", f"Un joueur avec l'ID {national_id} existe déjà."
                )
            return

        # Création et sauvegarde du joueur
        player = Player(last_name, first_name, birth_date, national_id)
        self.data_manager.save_player(player)

        # Réinitialisation du formulaire
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        # Mise à jour de la liste des joueurs
        self.load_players()

        # Confirmation
        messagebox.showinfo(
            "Succès", f"Le joueur {first_name} {last_name} a été enregistré."
            )

        # Passage à l'onglet de liste
        self.notebook.select(1)

    def load_players(self):
        """Charge et affiche la liste des joueurs"""
        # Effacement des données actuelles
        for item in self.players_table.get_children():
            self.players_table.delete(item)

        # Chargement des données
        data = self.data_manager.load_data()
        players = data.get("players", {})

        # Ajout des joueurs au tableau
        for national_id, player_data in players.items():
            self.players_table.insert(
                "",
                tk.END,
                values=(
                    national_id,
                    player_data["last_name"],
                    player_data["first_name"],
                    player_data["birth_date"]
                )
            )
