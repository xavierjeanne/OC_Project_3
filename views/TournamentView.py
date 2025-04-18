import tkinter as tk
from tkinter import ttk, messagebox


class TournamentView(ttk.Frame):
    """View for managing chess tournaments,
    including creation and management of tournaments"""

    def __init__(self, parent, **callbacks):
        """Initialize the tournament management view

        Args:
            parent: Parent widget containing this view
            callbacks: Dictionary containing
            callback functions for tournament operations
        """
        super().__init__(parent,
                         style='Main.TFrame')
        self.callbacks = callbacks
        self.edit_mode = False
        # Return button
        ttk.Button(self,
                   text="Retour à l'accueil",
                   command=self.callbacks.get('return_home'),
                   cursor='hand2',
                   style='Custom.TButton').grid(row=0,
                                                column=0,
                                                pady=10)

        # Create notebook
        self.notebook = ttk.Notebook(self,
                                     style='Custom.TNotebook')
        self.notebook.grid(row=1,
                           column=0,
                           sticky='nsew',
                           padx=10,
                           pady=10)

        # Create tournament tab
        self.add_tournament_frame = ttk.Frame(self.notebook,
                                              style='Main.TFrame')
        self.notebook.add(self.add_tournament_frame,
                          text="Ajouter un Tournoi")
        self._setup_add_tournament_tab()

        # Tournament list tab
        self.list_tournaments_frame = ttk.Frame(self.notebook,
                                                style='Main.TFrame')
        self.notebook.add(self.list_tournaments_frame,
                          text="Liste des Tournois")
        self._setup_list_tournaments_tab()

        self.grid_rowconfigure(1,
                               weight=1)
        self.grid_columnconfigure(0,
                                  weight=1)

    def _setup_add_tournament_tab(self):
        """Set up the tab for creating new tournaments

        adds a form with fields for:
        - Tournament name
        - Location
        - Start/End dates
        - Number of rounds
        - Description
        """
        for i in range(7):
            self.add_tournament_frame.grid_rowconfigure(i,
                                                        weight=1)
            self.add_tournament_frame.grid_columnconfigure(0,
                                                           weight=1)
            self.add_tournament_frame.grid_columnconfigure(1,
                                                           weight=2)

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
            ttk.Label(self.add_tournament_frame,
                      text=label_text,
                      style='Custom.TLabel').grid(row=idx,
                                                  column=0,
                                                  sticky='e',
                                                  padx=10,
                                                  pady=10)
            if field_name == "description":
                entry = tk.Text(self.add_tournament_frame,
                                height=2,
                                width=30)
            else:
                entry = ttk.Entry(self.add_tournament_frame,
                                  width=40)
            entry.grid(row=idx,
                       column=1,
                       sticky='w',
                       padx=10,
                       pady=10)
            self.entries[field_name] = entry

        ttk.Button(self.add_tournament_frame,
                   text="Enregistrer",
                   command=self.save_tournament,
                   style='Custom.TButton').grid(row=7,
                                                column=0,
                                                columnspan=2,
                                                pady=20)

    # In the _setup_list_tournaments_tab method, modify the tournament list display

    def _setup_list_tournaments_tab(self):
        """Set up the tab for displaying and managing tournaments

        Features:
        - Tournament list table
        - Player addition functionality
        - Tournament start option
        """
        self.list_tournaments_frame.grid_rowconfigure(0,
                                                      weight=1)
        self.list_tournaments_frame.grid_columnconfigure(0,
                                                         weight=1)

        # Update columns to include status
        columns = ("name",
                   "location",
                   "status",
                   "start_date",
                   "players",
                   "edit")
        self.tournaments_table = ttk.Treeview(self.list_tournaments_frame,
                                              columns=columns,
                                              show='headings',
                                              style='Custom.Treeview')

        headers = {
            "name": "Nom",
            "location": "Lieu",
            "status": "Statut",
            "start_date": "Date de début",
            "players": "Joueurs",
            "edit": "Editer"
        }

        for col, text in headers.items():
            if col == "edit":
                self.tournaments_table.heading(col,
                                               text=text,
                                               anchor='center')
                self.tournaments_table.column(col,
                                              width=70 ,
                                              anchor='center')
            else:
                self.tournaments_table.heading(col,
                                               text=text,
                                               anchor='nw')
                self.tournaments_table.column(col,
                                              width=150)

        # Add click event binding
        self.tournaments_table.bind('<ButtonRelease-1>',
                                    self.handle_click)

        self.tournaments_table.grid(row=0,
                                    column=0,
                                    sticky='nsew',
                                    padx=10,
                                    pady=10)
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_tournaments_frame,
                                  orient=tk.VERTICAL,
                                  command=self.tournaments_table.yview)
        self.tournaments_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,
                       column=1,
                       sticky='ns')

        # Buttons frame
        btn_frame = ttk.Frame(self.list_tournaments_frame,
                              style='Main.TFrame')
        btn_frame.grid(row=1,
                       column=0,
                       columnspan=2,
                       pady=10)

        ttk.Button(btn_frame,
                   text="Ajouter des joueurs",
                   command=self.add_players_to_tournament,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame,
                   text="Gestion du tournoi",
                   command=self.start_selected_tournament,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)

        self.load_tournaments()

    def save_tournament(self):
        tournament_data = {
            "name": self.entries["name"].get().strip(),
            "location": self.entries["location"].get().strip(),
            "start_date": self.entries["start_date"].get().strip(),
            "end_date": self.entries["end_date"].get().strip(),
            "rounds": self.entries["rounds"].get().strip() or "4",
            "description": self.entries["description"].get("1.0", tk.END).strip()
        }

        # Add the original name if in edit mode
        if self.edit_mode and hasattr(self,
                                      'current_tournament_name'):
            tournament_data["original_name"] = self.current_tournament_name

        success, message = self.callbacks.get('save_tournament')(tournament_data,
                                                                 self.edit_mode)
        if success:
            messagebox.showinfo("Succès",
                                message)
            self.reset_form()
            self.load_tournaments()
            self.notebook.select(1)
        else:
            messagebox.showerror("Erreur",
                                 message)

    def reset_form(self):
        """Reset the form to its initial state"""
        for field, entry in self.entries.items():
            if field == "description":
                entry.delete("1.0",
                             tk.END)
            else:
                entry.delete(0, tk.END)

        self.edit_mode = False
        self.current_tournament_name = None

    def handle_click(self, event):
        """Handle click events on the tournaments table"""
        region = self.tournaments_table.identify_region(event.x,
                                                        event.y)
        if region == "cell":
            item = self.tournaments_table.selection()[0]
            column = self.tournaments_table.identify_column(event.x)
            if column == '#6':
                values = self.tournaments_table.item(item)['values']

                if values[2] != "En cours" and values[2] != "Terminé":
                    self.fill_edit_form(values[0])
                else:
                    messagebox.showwarning("Edition impossible",
                                           "Impossible de modifier un tournoi démarré")

    def fill_edit_form(self, name):
        """Fill the tournament form with existing values for editing"""
        # Get full tournament data
        tournaments = self.callbacks.get('load_tournaments')()
        tournament_data = tournaments.get(name, {})

        if not tournament_data:
            return

        # Fill the form fields
        for field in ["name", "location", "start_date", "end_date", "rounds"]:
            if field in self.entries and field in tournament_data:
                self.entries[field].delete(0,
                                           tk.END)
                self.entries[field].insert(0,
                                           tournament_data[field])

        # Handle the description text widget separately
        if "description" in self.entries and "description" in tournament_data:
            self.entries["description"].delete("1.0",
                                               tk.END)
            self.entries["description"].insert("1.0",
                                               tournament_data["description"])

        # Update UI to reflect edit mode
        self.edit_mode = True
        self.current_tournament_name = name

        # Switch to the edit tab
        self.notebook.select(0)

    def load_tournaments(self):
        """Load and display all tournaments in the list"""
        # Clear existing items
        for item in self.tournaments_table.get_children():
            self.tournaments_table.delete(item)

        tournaments = self.callbacks.get('load_tournaments')()
        for name, tournament_data in tournaments.items():
            # Get status with default value if not present
            status = tournament_data.get("status",
                                         "Non démarré")

            self.tournaments_table.insert(
                "",
                tk.END,
                values=(
                    tournament_data["name"],
                    tournament_data["location"],
                    status,  # Add status here
                    tournament_data["start_date"],
                    len(tournament_data.get("players", [])),
                    "✏️"
                )
            )

    def add_players_to_tournament(self):
        selected = self.tournaments_table.selection()
        if not selected:
            messagebox.showwarning("Sélection requise",
                                   "Veuillez sélectionner un tournoi")
            return

        # Get the tournament name from the selected row
        item = selected[0]
        values = self.tournaments_table.item(item)['values']
        tournament_name = values[0]

        # Check tournament status
        tournaments = self.callbacks.get('load_tournaments')()
        tournament_data = tournaments.get(tournament_name, {})
        status = tournament_data.get('status', '')

        if status == "En cours" or status == "Terminé":
            messagebox.showwarning("Action impossible",
                                   "Impossible d'ajouter des joueurs à un tournoi"
                                   "démarré")
            return
        # Get the tournament name from the selected row
        item = selected[0]
        values = self.tournaments_table.item(item)['values']
        tournament_name = values[0]

        # Get tournament data to check existing players
        tournaments = self.callbacks.get('load_tournaments')()
        tournament_data = tournaments.get(tournament_name, {})
        existing_players = tournament_data.get('players', [])

        self.selection_window = tk.Toplevel(self)
        self.selection_window.title(f"Ajouter des joueurs - {tournament_name}")
        self.selection_window.geometry("400x500")

        players_frame = ttk.Frame(self.selection_window)
        players_frame.pack(fill=tk.BOTH,
                           expand=True,
                           padx=10,
                           pady=10)

        players = self.callbacks.get('load_available_players')()

        self.player_vars = {}
        for player_id, player_data in players.items():
            var = tk.BooleanVar()
            # Pre-select if player is already in the tournament
            if player_id in existing_players:
                var.set(True)
            self.player_vars[player_id] = var
            player_name = f"{player_data['last_name']} {player_data['first_name']}"
            ttk.Checkbutton(players_frame,
                            text=player_name,
                            variable=var).pack(anchor='w', pady=2)

        ttk.Button(self.selection_window,
                   text="Mettre à jour les joueurs",
                   command=lambda: self._confirm_add_players(tournament_name),
                   style='Custom.TButton').pack(pady=10)

    def _confirm_add_players(self, tournament_name):
        selected_players = [
            player_id for player_id, var in self.player_vars.items()
            if var.get()
        ]
        if selected_players:
            success, message = self.callbacks.get('add_players_to_tournament')(
                tournament_name,
                selected_players
            )
            # Check if the message contains a warning about player count
            if "Attention" in message:
                messagebox.showwarning("Attention", message)
            else:
                messagebox.showinfo("Succès", message)

                self.load_tournaments()
                # Close the selection window
                if hasattr(self,
                           'selection_window') and self.selection_window.winfo_exists():
                    self.selection_window.destroy()
                else:
                    messagebox.showerror("Erreur",
                                         message)
        else:
            messagebox.showwerror("Aucun joueur sélectionné",
                                  "Veuillez sélectionner au moins un joueur")

    def start_selected_tournament(self):
        selected = self.tournaments_table.selection()
        if not selected:
            messagebox.showwarning("Sélection requise",
                                   "Veuillez sélectionner un tournoi")
            return
        # Get the tournament name from the selected row
        item = selected[0]
        values = self.tournaments_table.item(item)['values']
        tournament_name = values[0]

        success, message = self.callbacks.get('open_round_page')(tournament_name)
        if success:
            messagebox.showinfo("Succès", message)
        else:
            messagebox.showerror("Erreur", message)
