import tkinter as tk
from tkinter import ttk, messagebox


class TournamentView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Main.TFrame')
        self.controller = controller

        # Return button
        ttk.Button(self,
                   text="Retour à l'accueil",
                   command=self.controller.return_home,
                   style='Custom.TButton').grid(row=0, column=0, pady=10)

        # Create notebook
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Create tournament tab
        self.create_tournament_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.create_tournament_frame, text="Nouveau Tournoi")
        self._setup_create_tournament_tab()

        # Tournament list tab
        self.list_tournaments_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.list_tournaments_frame, text="Liste des Tournois")
        self._setup_list_tournaments_tab()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _setup_create_tournament_tab(self):
        fields = [
            ("Nom du tournoi:", "name"),
            ("Lieu:", "location"),
            ("Date de début:", "start_date"),
            ("Date de fin:", "end_date"),
            ("Nombre de rounds:", "rounds"),
            ("Description:", "description")
        ]

        self.entries = {}
        for idx, (label_text, field_name) in enumerate(fields):
            ttk.Label(self.create_tournament_frame,
                      text=label_text).grid(row=idx, column=0, padx=10, pady=5)
            if field_name == "description":
                entry = tk.Text(self.create_tournament_frame, height=4, width=40)
            else:
                entry = ttk.Entry(self.create_tournament_frame, width=40)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[field_name] = entry

        ttk.Button(self.create_tournament_frame,
                   text="Créer le tournoi",
                   command=self.create_tournament,
                   style='Custom.TButton').grid(row=len(fields),
                                                column=0,
                                                columnspan=2,
                                                pady=20)

    def _setup_list_tournaments_tab(self):
        columns = ("name", "location", "start_date", "status", "players")
        self.tournaments_table = ttk.Treeview(self.list_tournaments_frame,
                                              columns=columns,
                                              show='headings')

        headers = {
            "name": "Nom",
            "location": "Lieu",
            "start_date": "Date de début",
            "status": "Statut",
            "players": "Joueurs"
        }

        for col, text in headers.items():
            self.tournaments_table.heading(col, text=text)
            self.tournaments_table.column(col, width=150)

        self.tournaments_table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_tournaments_frame,
                                  orient=tk.VERTICAL,
                                  command=self.tournaments_table.yview)
        self.tournaments_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Buttons frame
        btn_frame = ttk.Frame(self.list_tournaments_frame, style='Main.TFrame')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame,
                   text="Ajouter des joueurs",
                   command=self.add_players_to_tournament,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame,
                   text="Démarrer le tournoi",
                   command=self.start_selected_tournament,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)

        self.load_tournaments()

    def create_tournament(self):
        tournament_data = {
            "name": self.entries["name"].get(),
            "location": self.entries["location"].get(),
            "start_date": self.entries["start_date"].get(),
            "end_date": self.entries["end_date"].get(),
            "rounds": self.entries["rounds"].get() or "4",
            "description": self.entries["description"].get("1.0", tk.END).strip()
        }

        success, message = self.controller.create_tournament(tournament_data)
        if success:
            messagebox.showinfo("Succès", message)
            self.load_tournaments()
            self.notebook.select(1)
        else:
            messagebox.showerror("Erreur", message)

    def load_tournaments(self):
        for item in self.tournaments_table.get_children():
            self.tournaments_table.delete(item)

        tournaments = self.controller.load_tournaments()
        for tournament_id, tournament_data in tournaments.items():
            self.tournaments_table.insert(
                "",
                tk.END,
                values=(
                    tournament_data["name"],
                    tournament_data["location"],
                    tournament_data["start_date"],
                    tournament_data["status"],
                    len(tournament_data["players"])
                )
            )

    def add_players_to_tournament(self):
        """Add players to selected tournament"""
        selected = self.tournaments_table.selection()
        if not selected:
            messagebox.showwarning("Sélection requise",
                                   "Veuillez sélectionner un tournoi")
            return

        # Create player selection window
        selection_window = tk.Toplevel(self)
        selection_window.title("Ajouter des joueurs")
        selection_window.geometry("400x500")

        # Players listbox with checkboxes
        players_frame = ttk.Frame(selection_window)
        players_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get all players
        players = self.controller.load_available_players()
        # Create checkboxes for each player
        self.player_vars = {}
        for player_id, player_data in players.items():
            var = tk.BooleanVar()
            self.player_vars[player_id] = var
            player_name = f"{player_data['last_name']} {player_data['first_name']}"
            ttk.Checkbutton(players_frame,
                            text=player_name,
                            variable=var).pack(anchor='w', pady=2)

        # Add button
        ttk.Button(selection_window,
                   text="Ajouter les joueurs sélectionnés",
                   command=lambda: self._confirm_add_players(selected[0]),
                   style='Custom.TButton').pack(pady=10)

    def _confirm_add_players(self, tournament_id):
        """Confirm and add selected players to tournament"""
        selected_players = [
            player_id for player_id, var in self.player_vars.items()
            if var.get()
        ]
        if not selected_players:
            messagebox.showwarning("Sélection requise",
                                   "Veuillez sélectionner au moins un joueur")
            return

        success = self.controller.add_players_to_tournament(tournament_id,
                                                            selected_players)
        if success:
            messagebox.showinfo("Succès", "Joueurs ajoutés au tournoi")
            self.load_tournaments()
        else:
            messagebox.showerror("Erreur",
                                 "Impossible d'ajouter les joueurs au tournoi.\n"
                                 "Vérifiez que le tournoi n'a pas déjà commencé.")

    def start_selected_tournament(self):
        """Start the selected tournament"""
        selected = self.tournaments_table.selection()
        if not selected:
            messagebox.showwarning("Sélection requise",
                                   "Veuillez sélectionner un tournoi")
            return

        tournament_id = selected[0]
        success, message = self.controller.start_tournament(tournament_id)
        if success:
            messagebox.showinfo("Succès", message)
            self.load_tournaments()  # Refresh the tournaments list
        else:
            messagebox.showerror("Erreur", message)
