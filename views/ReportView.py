import tkinter as tk
from tkinter import ttk, messagebox


class ReportView(ttk.Frame):
    """View for displaying various reports"""

    def __init__(self, parent, **callbacks):
        """Initialize the report view

        Args:
            parent: Parent widget containing this view
            callbacks: Dictionary containing callback functions
            for report operations
        """
        super().__init__(parent,
                         style='Main.TFrame')
        self.callbacks = callbacks

        # Return button
        ttk.Button(self,
                   text="Retour à l'accueil",
                   command=self.callbacks.get('return_home'),
                   cursor='hand2',
                   style='Custom.TButton').grid(row=0, column=0, pady=10)

        # Create notebook for different reports
        self.notebook = ttk.Notebook(self,
                                     style='Custom.TNotebook')
        self.notebook.grid(row=1,
                           column=0,
                           sticky='nsew',
                           padx=10,
                           pady=10)

        # Players alphabetical tab
        self.players_frame = ttk.Frame(self.notebook,
                                       style='Main.TFrame')
        self.notebook.add(self.players_frame,
                          text="Liste des joueurs")
        self._setup_players_tab()

        # Tournaments list tab
        self.tournaments_frame = ttk.Frame(self.notebook,
                                           style='Main.TFrame')
        self.notebook.add(self.tournaments_frame,
                          text="Liste des tournois")
        self._setup_tournaments_tab()

        # Tournament details tab
        self.tournament_details_frame = ttk.Frame(self.notebook,
                                                  style='Main.TFrame')
        self.notebook.add(self.tournament_details_frame,
                          text="Détails d'un tournoi")
        self._setup_tournament_details_tab()

        # Tournament players tab
        self.tournament_players_frame = ttk.Frame(self.notebook,
                                                  style='Main.TFrame')
        self.notebook.add(self.tournament_players_frame,
                          text="Joueurs d'un tournoi")
        self._setup_tournament_players_tab()

        # Tournament rounds and matches tab
        self.rounds_matches_frame = ttk.Frame(self.notebook,
                                              style='Main.TFrame')
        self.notebook.add(self.rounds_matches_frame,
                          text="Tours et matchs")
        self._setup_rounds_matches_tab()

        # Tournament scores tab
        self.scores_frame = ttk.Frame(self.notebook,
                                      style='Main.TFrame')
        self.notebook.add(self.scores_frame,
                          text="Scores")
        self._setup_scores_tab()
        # Initialize tournament selectors
        self.update_tournament_selectors()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _setup_players_tab(self):
        """Set up the tab for displaying all players alphabetically"""
        self.players_frame.grid_rowconfigure(0,
                                             weight=1)
        self.players_frame.grid_columnconfigure(0,
                                                weight=1)

        # Create players table
        columns = ("name",
                   "first_name",
                   "birth_date",
                   "national_id")
        self.players_table = ttk.Treeview(self.players_frame,
                                          columns=columns,
                                          show='headings',
                                          style='Custom.Treeview')

        headers = {
            "name": "Nom",
            "first_name": "Prénom",
            "birth_date": "Date de naissance",
            "national_id": "ID National"
        }

        for col, text in headers.items():
            self.players_table.heading(col,
                                       text=text,
                                       anchor='nw')
            self.players_table.column(col,
                                      width=150)

        self.players_table.grid(row=0,
                                column=0,
                                sticky='nsew', padx=10, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.players_frame,
                                  orient=tk.VERTICAL,
                                  command=self.players_table.yview)
        self.players_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.load_players_alphabetical()

    def _setup_tournaments_tab(self):
        """Set up the tab for displaying all tournaments"""
        self.tournaments_frame.grid_rowconfigure(0,
                                                 weight=1)
        self.tournaments_frame.grid_columnconfigure(0,
                                                    weight=1)

        # Create tournaments table
        columns = ("name",
                   "location",
                   "start_date",
                   "end_date",
                   "status")
        self.tournaments_table = ttk.Treeview(self.tournaments_frame,
                                              columns=columns,
                                              show='headings',
                                              style='Custom.Treeview')

        headers = {
            "name": "Nom",
            "location": "Lieu",
            "start_date": "Date de début",
            "end_date": "Date de fin",
            "status": "Statut"
        }

        for col, text in headers.items():
            self.tournaments_table.heading(col,
                                           text=text,
                                           anchor='nw')
            self.tournaments_table.column(col,
                                          width=150)

        self.tournaments_table.grid(row=0,
                                    column=0,
                                    sticky='nsew',
                                    padx=10,
                                    pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tournaments_frame,
                                  orient=tk.VERTICAL,
                                  command=self.tournaments_table.yview)
        self.tournaments_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,
                       column=1,
                       sticky='ns')

        self.load_tournaments()

    def _setup_tournament_details_tab(self):
        """Set up the tab for displaying details
        of a specific tournament"""
        # Tournament selection
        selection_frame = ttk.Frame(self.tournament_details_frame,
                                    style='Main.TFrame')
        selection_frame.pack(fill=tk.X,
                             padx=10,
                             pady=10)

        ttk.Label(selection_frame,
                  text="Sélectionner un tournoi:").pack(side=tk.LEFT,
                                                        padx=5)
        self.tournament_selector = ttk.Combobox(selection_frame,
                                                width=30)
        self.tournament_selector.pack(side=tk.LEFT,
                                      padx=5)
        ttk.Button(selection_frame,
                   text="Afficher",
                   command=self.load_tournament_details,
                   style='Custom.TButton').pack(side=tk.LEFT,
                                                padx=5)

        table_frame = ttk.Frame(self.tournament_details_frame,
                                style='Main.TFrame')
        table_frame.pack(fill=tk.BOTH,
                         expand=True,
                         padx=10,
                         pady=10)
        table_frame.grid_rowconfigure(0,
                                      weight=1)
        table_frame.grid_columnconfigure(0,
                                         weight=1)

        # Fix: Define column IDs that match the headers
        columns = ("name",
                   "location",
                   "start_date",
                   "end_date",
                   "rounds",
                   "description",
                   "status")
        self.tournament_table_detail = ttk.Treeview(table_frame,
                                                    columns=columns,
                                                    show='headings',
                                                    style='Custom.Treeview')
        headers = {
            "name": "Nom",
            "location": "Lieu",
            "start_date": "Date de début",
            "end_date": "Date de fin",
            "rounds": "Nombre de tours",
            "description": "Description",
            "status": "Statut"
        }

        for col, text in headers.items():
            self.tournament_table_detail.heading(col,
                                                 text=text,
                                                 anchor='nw')
            self.tournament_table_detail.column(col,
                                                width=150)

        self.tournament_table_detail.grid(row=0,
                                          column=0,
                                          sticky='nsew')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient=tk.VERTICAL,
                                  command=self.tournament_table_detail.yview)
        self.tournament_table_detail.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,
                       column=1,
                       sticky='ns')

    def _setup_tournament_players_tab(self):
        """Set up the tab for displaying
        players of a specific tournament"""
        # Tournament selection
        selection_frame = ttk.Frame(self.tournament_players_frame,
                                    style='Main.TFrame')
        selection_frame.pack(fill=tk.X,
                             padx=10,
                             pady=10)

        ttk.Label(selection_frame,
                  text="Sélectionner un tournoi:").pack(side=tk.LEFT,
                                                        padx=5)
        self.players_tournament_selector = ttk.Combobox(selection_frame,
                                                        width=30)
        self.players_tournament_selector.pack(side=tk.LEFT,
                                              padx=5)
        ttk.Button(selection_frame,
                   text="Afficher",
                   command=self.load_tournament_players,
                   style='Custom.TButton').pack(side=tk.LEFT,
                                                padx=5)

        # Players table
        table_frame = ttk.Frame(self.tournament_players_frame,
                                style='Main.TFrame')
        table_frame.pack(fill=tk.BOTH,
                         expand=True,
                         padx=10,
                         pady=10)
        table_frame.grid_rowconfigure(0,
                                      weight=1)
        table_frame.grid_columnconfigure(0,
                                         weight=1)

        columns = ("last_name",
                   "first_name",
                   "birth_date",
                   "national_id")
        self.tournament_players_table = ttk.Treeview(table_frame,
                                                     columns=columns,
                                                     show='headings',
                                                     style='Custom.Treeview')

        headers = {
            "last_name": "Nom",
            "first_name": "Prénom",
            "birth_date": "Date de naissance",
            "national_id": "ID National"
        }

        for col, text in headers.items():
            self.tournament_players_table.heading(col,
                                                  text=text,
                                                  anchor='nw')
            self.tournament_players_table.column(col,
                                                 width=150)

        self.tournament_players_table.grid(row=0,
                                           column=0,
                                           sticky='nsew')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient=tk.VERTICAL,
                                  command=self.tournament_players_table.yview)
        self.tournament_players_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,
                       column=1,
                       sticky='ns')

    def _setup_rounds_matches_tab(self):
        """Set up the tab for displaying rounds and matches
        of a specific tournament"""
        # Tournament selection
        selection_frame = ttk.Frame(self.rounds_matches_frame,
                                    style='Main.TFrame')
        selection_frame.pack(fill=tk.X,
                             padx=10,
                             pady=10)

        ttk.Label(selection_frame,
                  text="Sélectionner un tournoi:").pack(side=tk.LEFT,
                                                        padx=5)
        self.rounds_tournament_selector = ttk.Combobox(selection_frame,
                                                       width=30)
        self.rounds_tournament_selector.pack(side=tk.LEFT,
                                             padx=5)
        ttk.Button(selection_frame,
                   text="Afficher",
                   command=self.load_tournament_rounds_matches,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)

        # Rounds and matches frame
        self.rounds_matches_container = ttk.Frame(self.rounds_matches_frame,
                                                  style='Main.TFrame')
        self.rounds_matches_container.pack(fill=tk.BOTH,
                                           expand=True,
                                           padx=10,
                                           pady=10)

    def _setup_scores_tab(self):
        """Set up the tab for displaying scores
        of a specific tournament"""
        # Tournament select ion
        selection_frame = ttk.Frame(self.scores_frame,
                                    style='Main.TFrame')
        selection_frame.pack(fill=tk.X,
                             padx=10,
                             pady=10)

        ttk.Label(selection_frame,
                  text="Sélectionner un tournoi:").pack(side=tk.LEFT,
                                                        padx=5)
        self.scores_selector = ttk.Combobox(selection_frame,
                                            width=30)
        self.scores_selector.pack(side=tk.LEFT,
                                  padx=5)
        ttk.Button(selection_frame,
                   text="Afficher",
                   command=self.load_scores,
                   style='Custom.TButton').pack(side=tk.LEFT,
                                                padx=5)

        # Players table
        table_frame = ttk.Frame(self.scores_frame,
                                style='Main.TFrame')
        table_frame.pack(fill=tk.BOTH,
                         expand=True,
                         padx=10,
                         pady=10)
        table_frame.grid_rowconfigure(0,
                                      weight=1)
        table_frame.grid_columnconfigure(0,
                                         weight=1)

        columns = ("rank",
                   "last_name",
                   "first_name",
                   "score")
        self.scores_table = ttk.Treeview(table_frame,
                                         columns=columns,
                                         show='headings',
                                         style='Custom.Treeview')

        headers = {
            "rank": "Classement",
            "last_name": "Nom",
            "first_name": "Prénom",
            "score": "score"
        }

        for col, text in headers.items():
            self.scores_table.heading(col,
                                      text=text,
                                      anchor='nw')
            self.scores_table.column(col,
                                     width=150)

        self.scores_table.grid(row=0,
                               column=0,
                               sticky='nsew')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient=tk.VERTICAL,
                                  command=self.scores_table.yview)
        self.scores_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,
                       column=1,
                       sticky='ns')

    def load_players_alphabetical(self):
        """Load and display all players in alphabetical order"""
        # Clear existing items
        for item in self.players_table.get_children():
            self.players_table.delete(item)

        # Get pre-sorted players data from controller
        sorted_players = self.callbacks.get('get_players_alphabetical')()

        # Display players
        for player in sorted_players:
            self.players_table.insert(
                "",
                tk.END,
                values=(
                    player.get('last_name', ''),
                    player.get('first_name', ''),
                    player.get('birth_date', ''),
                    player.get('id', '')
                )
            )

    def load_tournaments(self):
        """Load and display all tournaments"""
        # Clear existing items
        for item in self.tournaments_table.get_children():
            self.tournaments_table.delete(item)

        # Get formatted tournaments data from controller
        tournaments = self.callbacks.get('get_tournaments_for_display')()

        # Update tournament selectors
        self.update_tournament_selectors()

        # Display tournaments
        for tournament in tournaments:
            self.tournaments_table.insert(
                "",
                tk.END,
                values=(
                    tournament.get('name', ''),
                    tournament.get('location', ''),
                    tournament.get('start_date', ''),
                    tournament.get('end_date', ''),
                    tournament.get('status', 'Non démarré')
                )
            )

    def load_tournament_details(self):
        """Load and display details of the selected tournament"""
        tournament_name = self.tournament_selector.get()

        # Let controller handle validation and data retrieval
        result = (self.
                  callbacks.get('get_tournament_details_for_display')(tournament_name))

        if not result['success']:
            messagebox.showwarning("Avertissement",
                                   result['message'])
            return

        # Clear existing items
        for item in self.tournament_table_detail.get_children():
            self.tournament_table_detail.delete(item)

        # Display tournament details
        tournament = result['data']
        self.tournament_table_detail.insert(
            "",
            tk.END,
            values=(
                tournament.get('name', ''),
                tournament.get('location', ''),
                tournament.get('start_date', ''),
                tournament.get('end_date', ''),
                tournament.get('rounds', ''),
                tournament.get('description', ''),
                tournament.get('status', 'Non démarré')
            )
        )

    def load_scores(self):
        """Load and display scores of the selected tournament"""
        tournament_name = self.scores_selector.get()

        # Let controller handle validation and data retrieval
        result = (self.callbacks.get('get_tournament_standings_for_display')
                  (tournament_name))

        if not result['success']:
            messagebox.showwarning("Avertissement",
                                   result['message'])
            return

        # Clear existing items
        for item in self.scores_table.get_children():
            self.scores_table.delete(item)

        # Display tournament scores - fixed to handle a list of players with scores
        scores = result['data']
        for score in scores:
            self.scores_table.insert(
                "",
                tk.END,
                values=(
                    score.get('rank', ''),
                    score.get('last_name', ''),
                    score.get('first_name', ''),
                    score.get('score', '')
                )
            )

    def load_tournament_players(self):
        """Load and display players of the selected tournament"""
        tournament_name = self.players_tournament_selector.get()

        # Let controller handle validation and data retrieval
        result = (self.callbacks.get('get_tournament_players_for_display')
                  (tournament_name))

        if not result['success']:
            messagebox.showwarning("Avertissement",
                                   result['message'])
            return

        # Clear existing items
        for item in self.tournament_players_table.get_children():
            self.tournament_players_table.delete(item)

        # Display players
        players = result['data']
        for player in players:
            self.tournament_players_table.insert(
                "",
                tk.END,
                values=(
                    player.get('last_name', ''),
                    player.get('first_name', ''),
                    player.get('birth_date', ''),
                    player.get('id', '')
                )
            )

    def load_tournament_rounds_matches(self):
        """Load and display rounds and matches of the selected tournament"""
        tournament_name = self.rounds_tournament_selector.get()

        # Let controller handle validation and data retrieval
        # The issue is here - you need to call the method, not just reference it
        result = self.callbacks.get(
            'get_tournament_rounds_matches_for_display')(tournament_name)

        if not result['success']:
            messagebox.showwarning("Avertissement",
                                   result['message'])
            return

        # Clear existing widgets
        for widget in self.rounds_matches_container.winfo_children():
            widget.destroy()

        # Create a canvas with scrollbar for potentially many rounds
        canvas = tk.Canvas(self.rounds_matches_container)
        scrollbar = ttk.Scrollbar(self.rounds_matches_container,
                                  orient="vertical",
                                  command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas,
                                     style='Main.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left",
                    fill="both",
                    expand=True)
        scrollbar.pack(side="right",
                       fill="y")

        # Display rounds and matches using pre-processed data from controller
        rounds_data = result['data']
        for i, round_data in enumerate(rounds_data):
            round_frame = ttk.LabelFrame(
                scrollable_frame,
                text=f"{round_data.get('name', f'Tour {i+1}')}",
                style='Custom.TLabelframe'
            )
            round_frame.pack(fill="x",
                             expand=True,
                             padx=10,
                             pady=5)

            # Round details
            ttk.Label(
                round_frame,
                text=f"Début: {round_data.get('start_time', 'Non démarré')}"
            ).pack(anchor="w",
                   padx=5,
                   pady=2)

            ttk.Label(
                round_frame,
                text=f"Fin: {round_data.get('end_time', 'En cours')}"
            ).pack(anchor="w",
                   padx=5,
                   pady=2)

            # Matches
            matches = round_data.get('matches', [])
            if not matches:
                ttk.Label(round_frame,
                          text="Aucun match").pack(padx=5,
                                                   pady=5)
                continue

            # Create a table for matches
            match_table_frame = ttk.Frame(round_frame,
                                          style='Main.TFrame')
            match_table_frame.pack(fill="both",
                                   expand=True,
                                   padx=10,
                                   pady=5)

            # Configure the frame to expand properly
            match_table_frame.columnconfigure(0,
                                              weight=1)
            match_table_frame.rowconfigure(0,
                                           weight=1)

            # Create table headers
            columns = ("match_num",
                       "player1",
                       "score1",
                       "player2",
                       "score2")
            match_table = ttk.Treeview(match_table_frame,
                                       columns=columns,
                                       show='headings',
                                       style='Custom.Treeview',
                                       height=len(matches))

            # Configure headers
            match_table.heading("match_num",
                                text="Match",
                                anchor='w')
            match_table.heading("player1",
                                text="Joueur 1",
                                anchor='w')
            match_table.heading("score1",
                                text="Score",
                                anchor='center')
            match_table.heading("player2",
                                text="Joueur 2",
                                anchor='w')
            match_table.heading("score2",
                                text="Score",
                                anchor='center')

            # Configure column widths with proper proportions
            match_table.column("match_num",
                               width=80,
                               minwidth=60)
            match_table.column("player1",
                               width=200,
                               minwidth=120)
            match_table.column("score1",
                               width=60,
                               minwidth=40,
                               anchor='center')
            match_table.column("player2",
                               width=200,
                               minwidth=120)
            match_table.column("score2",
                               width=60,
                               minwidth=40,
                               anchor='center')

            # Use grid instead of pack for better control
            match_table.grid(row=0,
                             column=0,
                             sticky='nsew')

            # Add matches to the table - now using pre-formatted data from controller
            for j, match in enumerate(matches):
                match_table.insert(
                    "",
                    tk.END,
                    values=(
                        f"Match {j+1}",
                        match.get('player1_name', ''),
                        match.get('score1', ''),
                        match.get('player2_name', ''),
                        match.get('score2', '')
                    )
                )

    def update_tournament_selectors(self):
        """Update all tournament selector comboboxes"""
        # Get tournament names from controller
        tournament_names = self.callbacks.get('get_tournament_names')()

        # Update all selectors
        if hasattr(self,
                   'tournament_selector'):
            self.tournament_selector['values'] = tournament_names
        if hasattr(self,
                   'players_tournament_selector'):
            self.players_tournament_selector['values'] = tournament_names
        if hasattr(self,
                   'rounds_tournament_selector'):
            self.rounds_tournament_selector['values'] = tournament_names
        if hasattr(self,
                   'scores_selector'):
            self.scores_selector['values'] = tournament_names

    def refresh_data(self):
        """Refresh all data in the report view when it becomes visible again"""
        # Reload all data
        self.load_players_alphabetical()
        self.load_tournaments()
        self.update_tournament_selectors()

        # Refresh the currently selected tab data if needed
        current_tab = self.notebook.select()
        tab_id = self.notebook.index(current_tab)

        # Refresh specific tab data based on which tab is active
        if tab_id == 2:  # Tournament details tab
            if self.tournament_selector.get():
                self.load_tournament_details()
        elif tab_id == 3:  # Tournament players tab
            if self.players_tournament_selector.get():
                self.load_tournament_players()
        elif tab_id == 4:  # Rounds and matches tab
            if self.rounds_tournament_selector.get():
                self.load_tournament_rounds_matches()
        elif tab_id == 5:  # Scores tab
            if self.scores_selector.get():
                self.load_scores()
