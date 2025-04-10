import tkinter as tk
from tkinter import ttk, messagebox


class RoundView(ttk.Frame):
    """View for managing chess rounds,
    including creation and management of rounds"""

    def __init__(self, parent, **callbacks):
        """Initialize the round management view

        Args:
            parent: Parent widget containing this view
            callbacks: Dictionary containing callback functions for round operations
        """
        super().__init__(parent, style='Main.TFrame')
        self.callbacks = callbacks
        self.edit_mode = False
        self.tournament_data = None

        # Return button
        ttk.Button(self,
                   text="Retour à la liste des tournois",
                   command=self.callbacks.get('return_list_tournament'),
                   cursor='hand2',
                   style='Custom.TButton').grid(row=0, column=0, pady=10)

        # Create notebook
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # round list tab
        self.list_rounds_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.list_rounds_frame, text="Liste des tours")
        self._setup_list_rounds_tab()

        # Create round tab
        self.list_scores_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.list_scores_frame, text="Score des matchs")
        self._setup_list_scores_tab()

        self.ranking_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.ranking_frame, text="Classement des joueurs")
        self._setup_ranking_tab()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Don't load tournament data immediately
        # We'll load it when the view is shown

    def show(self):
        """Called when the view is shown to load tournament data"""
        # Clear existing items in tables
        for item in self.rounds_table.get_children():
            self.rounds_table.delete(item)
        
        for item in self.matches_table.get_children():
            self.matches_table.delete(item)
        
        for item in self.rankings_table.get_children():
            self.rankings_table.delete(item)
        
        # Load tournament data
        self.load_tournament_data()

    def load_tournament_data(self):
        """Load current tournament data from controller"""
        get_tournament = self.callbacks.get('get_current_tournament')
        if get_tournament:
            self.tournament_data = get_tournament()
            if self.tournament_data:
                self.load_rounds()
                self.load_matches()
                self.update_rankings()

    def _setup_list_rounds_tab(self):
        """Set up the tab for displaying and managing rounds"""
        self.list_rounds_frame.grid_rowconfigure(0, weight=1)
        self.list_rounds_frame.grid_columnconfigure(0, weight=1)

        # Create rounds table
        columns = ("name", "start_time", "end_time", "status")
        self.rounds_table = ttk.Treeview(self.list_rounds_frame,
                                         columns=columns,
                                         show='headings',
                                         style='Custom.Treeview')

        headers = {
            "name": "Nom du tour",
            "start_time": "Date et heure de début",
            "end_time": "Date et heure de fin",
            "status": "Statut"
        }

        for col, text in headers.items():
            self.rounds_table.heading(col, text=text, anchor='nw')
            self.rounds_table.column(col, width=150)

        self.rounds_table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_rounds_frame,
                                  orient=tk.VERTICAL,
                                  command=self.rounds_table.yview)
        self.rounds_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Buttons frame
        btn_frame = ttk.Frame(self.list_rounds_frame, style='Main.TFrame')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame,
                   text="Créer un nouveau tour",
                   command=self.create_new_round,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame,
                   text="Terminer le tour sélectionné",
                   command=self.finish_selected_round,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
    def _setup_list_scores_tab(self):
        """Set up the tab for managing match scores"""
        self.list_scores_frame.grid_rowconfigure(0, weight=1)
        self.list_scores_frame.grid_columnconfigure(0, weight=1)

        # Create matches table
        columns = ("round", "player1", "score1", "player2", "score2")
        self.matches_table = ttk.Treeview(self.list_scores_frame,
                                          columns=columns,
                                          show='headings',
                                          style='Custom.Treeview')

        headers = {
            "round": "Tour",
            "player1": "Joueur 1 (Blanc)",
            "score1": "Score",
            "player2": "Joueur 2 (Noir)",
            "score2": "Score"
        }

        for col, text in headers.items():
            self.matches_table.heading(col, text=text, anchor='nw')
            if col in ["score1", "score2"]:
                self.matches_table.column(col, width=50, anchor='center')
            else:
                self.matches_table.column(col, width=150)

        self.matches_table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_scores_frame,
                                  orient=tk.VERTICAL,
                                  command=self.matches_table.yview)
        self.matches_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Buttons frame
        btn_frame = ttk.Frame(self.list_scores_frame, style='Main.TFrame')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame,
                   text="Mettre à jour les scores",
                   command=self.update_match_scores,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        self.load_matches()  # Load matches when the view is shown
    def _setup_ranking_tab(self):
        """Set up the tab for displaying player rankings"""
        self.ranking_frame.grid_rowconfigure(0, weight=1)
        self.ranking_frame.grid_columnconfigure(0, weight=1)

        # Create rankings table
        columns = ("rank", "player", "points")
        self.rankings_table = ttk.Treeview(self.ranking_frame,
                                           columns=columns,
                                           show='headings',
                                           style='Custom.Treeview')

        headers = {
            "rank": "Rang",
            "player": "Joueur",
            "points": "Points"
        }

        for col, text in headers.items():
            self.rankings_table.heading(col, text=text, anchor='nw')
            if col == "rank":
                self.rankings_table.column(col, width=50, anchor='center')
            elif col == "points":
                self.rankings_table.column(col, width=100, anchor='center')
            else:
                self.rankings_table.column(col, width=250)

        self.rankings_table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.ranking_frame,
                                  orient=tk.VERTICAL,
                                  command=self.rankings_table.yview)
        self.rankings_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Refresh button
        ttk.Button(self.ranking_frame,
                   text="Rafraîchir le classement",
                   command=self.update_rankings,
                   style='Custom.TButton').grid(row=1, column=0, pady=10)
        self.load_player_rankings()  # Load rankings when the view is shown
        
    def load_player_rankings(self):
        """Load and display player rankings for the current tournament"""
        # Clear existing items first
        for item in self.rankings_table.get_children():
            self.rankings_table.delete(item)
        
        # Rest of your load_player_rankings code...
    def load_rounds(self):
        """Load and display rounds for the current tournament"""
        # Clear existing items first
        for item in self.rounds_table.get_children():
            self.rounds_table.delete(item)
        
        rounds_data = self.tournament_data.get('rounds_data', [])

        for round_data in rounds_data:
            status = "Terminé" if round_data.get('end_time') else "En cours"
            self.rounds_table.insert(
                "",
                tk.END,
                values=(
                    round_data.get('name', ''),
                    round_data.get('start_time', ''),
                    round_data.get('end_time', ''),
                    status
                )
            )

    def load_matches(self):
        """Load and display matches for the current tournament"""
        # Clear existing items first
        for item in self.matches_table.get_children():
            self.matches_table.delete(item)
        
        if not self.tournament_data:
            return
        
        # Get player names dictionary for display
        player_names = {}
        if self.callbacks.get('get_player_names'):
            player_names = self.callbacks.get('get_player_names')()
        
        # Load matches from all rounds
        rounds_data = self.tournament_data.get('rounds_data', [])
        
        for round_data in rounds_data:
            round_name = round_data.get('name', '')
            
            for match in round_data.get('matches', []):
                if isinstance(match, list) and len(match) == 2:
                    player1_id, score1 = match[0]
                    player2_id, score2 = match[1]
                    
                    player1_name = player_names.get(player1_id, f"Joueur {player1_id}")
                    player2_name = player_names.get(player2_id, f"Joueur {player2_id}")
                    
                    self.matches_table.insert(
                        "",
                        tk.END,
                        values=(
                            round_name,
                            player1_name,
                            score1,
                            player2_name,
                            score2
                        ),
                        tags=(player1_id, player2_id)  # Store player IDs as tags for later use
                    )

    def update_rankings(self):
        """Update the player rankings display"""
        # Clear existing items first
        for item in self.rankings_table.get_children():
            self.rankings_table.delete(item)
        
        if not self.tournament_data:
            return
        
        # Get player points
        player_points = {}
        if self.callbacks.get('calculate_player_points'):
            player_points = self.callbacks.get('calculate_player_points')()
        
        # Get player names
        player_names = {}
        if self.callbacks.get('get_player_names'):
            player_names = self.callbacks.get('get_player_names')()
        
        # Sort players by points
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        
        # Display rankings
        for rank, (player_id, points) in enumerate(sorted_players, 1):
            player_name = player_names.get(player_id, f"Joueur {player_id}")
            
            self.rankings_table.insert(
                "",
                tk.END,
                values=(
                    rank,
                    player_name,
                    points
                )
            )

    def create_new_round(self):
        """Create a new round with paired players"""
        success, message = self.callbacks.get('create_new_round')()
        if success:
            messagebox.showinfo("Succès", message)
            self.load_tournament_data()
        else:
            messagebox.showerror("Erreur", message)

    def finish_selected_round(self):
        """Mark the selected round as finished"""
        selection = self.rounds_table.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un tour")
            return

        item = selection[0]
        round_name = self.rounds_table.item(item)['values'][0]

        success, message = self.callbacks.get('finish_round')(round_name)
        if success:
            messagebox.showinfo("Succès", message)
            self.load_tournament_data()
        else:
            messagebox.showerror("Erreur", message)

    def update_match_scores(self):
        """Open a dialog to update scores for the selected match"""
        selection = self.matches_table.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un match")
            return

        item = selection[0]
        values = self.matches_table.item(item)['values']
        tags = self.matches_table.item(item)['tags']

        round_name = values[0]
        player1_id, player2_id = tags[0], tags[1]

        # Create score update dialog
        self.score_dialog = tk.Toplevel(self)
        self.score_dialog.title("Mettre à jour les scores")
        self.score_dialog.geometry("400x200")
        self.score_dialog.resizable(False, False)

        ttk.Label(self.score_dialog,
                  text=f"Match: {values[1]} vs {values[3]}").pack(pady=10)

        score_frame = ttk.Frame(self.score_dialog)
        score_frame.pack(pady=10)

        ttk.Label(score_frame,
                  text=f"{values[1]}:").grid(row=0, column=0, padx=5, pady=5)
        score1_var = tk.StringVar(value=values[2])
        score1_combo = ttk.Combobox(score_frame,
                                    textvariable=score1_var,
                                    values=["0", "0.5", "1"], width=5)
        score1_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(score_frame, text=f"{values[3]}:").grid(row=1,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        score2_var = tk.StringVar(value=values[4])
        score2_combo = ttk.Combobox(score_frame,
                                    textvariable=score2_var,
                                    values=["0", "0.5", "1"],
                                    width=5)
        score2_combo.grid(row=1, column=1, padx=5, pady=5)

        def save_scores():
            try:
                score1 = float(score1_var.get())
                score2 = float(score2_var.get())

                # Validate scores
                if score1 + score2 > 1:
                    messagebox.showerror("Erreur",
                                         "La somme des scores ne peut pas dépasser 1")
                    return

                success, message = self.callbacks.get('update_match_scores')(
                    round_name, player1_id, player2_id, score1, score2
                )

                if success:
                    messagebox.showinfo("Succès", message)
                    self.score_dialog.destroy()
                    self.load_tournament_data()
                else:
                    messagebox.showerror("Erreur", message)
            except ValueError:
                messagebox.showerror("Erreur",
                                     "Les scores doivent être des nombres valides")

        ttk.Button(self.score_dialog, text="Enregistrer",
                   command=save_scores).pack(pady=10)
