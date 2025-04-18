import tkinter as tk
from tkinter import ttk, messagebox


class PlayerView(ttk.Frame):
    """View for managing chess players,
    including adding new players and viewing player list"""

    def __init__(self, parent, **callbacks):
        """Initialize the player management view

        Args:
            parent: Parent widget containing this view
            callbacks: Dictionary containing callback functions for player operations
        """
        super().__init__(parent,
                         style='Main.TFrame')
        self.callbacks = callbacks
        self.original_id = None
        self.edit_mode = False
        # Return button
        ttk.Button(self,
                   text="Retour à l'accueil",
                   command=self.callbacks.get('return_home'),
                   cursor='hand2',
                   style='Custom.TButton').grid(row=0, column=0, pady=10)

        # Create notebook
        self.notebook = ttk.Notebook(self,
                                     style='Custom.TNotebook')
        self.notebook.grid(row=1,
                           column=0,
                           sticky='nsew',
                           padx=10,
                           pady=10)

        # Add player tab
        self.add_player_frame = ttk.Frame(self.notebook,
                                          style='Main.TFrame')
        self.notebook.add(self.add_player_frame,
                          text="Ajouter un joueur")
        self._setup_add_player_tab()

        # Players list tab
        self.list_players_frame = ttk.Frame(self.notebook,
                                            style='Main.TFrame')
        self.notebook.add(self.list_players_frame,
                          text="Liste des joueurs")
        self._setup_list_players_tab()

        # Configure weights
        self.grid_rowconfigure(1,
                               weight=1)
        self.grid_columnconfigure(0,
                                  weight=1)

    def _setup_add_player_tab(self):
        """Set up the tab for adding new players

        Creates a form with fields for:
        - Last name
        - First name
        - Birth date
        - National ID
        """
        for i in range(5):
            self.add_player_frame.grid_rowconfigure(i,
                                                    weight=1)
            self.add_player_frame.grid_columnconfigure(0,
                                                       weight=1)
            self.add_player_frame.grid_columnconfigure(1,
                                                       weight=2)

        fields = [
            ("Nom:", "last_name"),
            ("Prénom:", "first_name"),
            ("Date de naissance (JJ/MM/AAAA):", "birth_date"),
            ("Identifiant national:", "national_id")
        ]

        self.entries = {}
        for idx, (label_text,
                  field_name) in enumerate(fields):
            ttk.Label(self.add_player_frame,
                      text=label_text,
                      style='Custom.TLabel').grid(row=idx,
                                                  column=0,
                                                  sticky='e',
                                                  padx=10,
                                                  pady=10)

            entry = ttk.Entry(self.add_player_frame,
                              width=40)
            entry.grid(row=idx,
                       column=1,
                       sticky='w',
                       padx=10,
                       pady=10)
            self.entries[field_name] = entry

        ttk.Button(self.add_player_frame,
                   text="Enregistrer",
                   command=self.save_player,
                   style='Custom.TButton'
                   ).grid(row=4,
                          column=0,
                          columnspan=2,
                          pady=20)

    def _setup_list_players_tab(self):
        """Set up the tab for displaying the list of players

        Features:
        - Sortable columns
        - Scrollable view
        - Columns for ID, name, and birth date
        """
        self.list_players_frame.grid_rowconfigure(0,
                                                  weight=1)
        self.list_players_frame.grid_columnconfigure(0,
                                                     weight=1)

        columns = ("national_id",
                   "last_name",
                   "first_name",
                   "birth_date",
                   "edit")

        self.players_table = ttk.Treeview(self.list_players_frame,
                                          columns=columns,
                                          show='headings',
                                          style='Custom.Treeview'
                                          )

        headers = {
            "national_id": "ID National",
            "last_name": "Nom",
            "first_name": "Prénom",
            "birth_date": "Date de naissance",
            "edit": "Éditer"
        }

        for col, text in headers.items():
            if col == "edit":
                self.players_table.heading(col,
                                           text=text,
                                           anchor='center')
                self.players_table.column(col,
                                          width=70,
                                          anchor='center')
            else:
                self.players_table.heading(col,
                                           text=text,
                                           anchor='nw')
                self.players_table.column(col,
                                          width=150)

        # Add click event binding
        self.players_table.bind('<ButtonRelease-1>',
                                self.handle_click)

        scrollbar = ttk.Scrollbar(self.list_players_frame,
                                  orient=tk.VERTICAL,
                                  command=self.players_table.yview)
        self.players_table.configure(yscroll=scrollbar.set)

        self.players_table.grid(row=0,
                                column=0,
                                sticky='nsew')
        scrollbar.grid(row=0,
                       column=1,
                       sticky='ns')

        self.load_players()

    def save_player(self):
        """Save new player data from the form"""
        player_data = {
            "last_name": self.entries["last_name"].get().strip(),
            "first_name": self.entries["first_name"].get().strip(),
            "birth_date": self.entries["birth_date"].get().strip(),
            "national_id": self.entries["national_id"].get().strip()
        }

        # Add the original ID if in edit mode
        if self.edit_mode:
            player_data["original_id"] = self.original_id

        success, message = self.callbacks.get('save_player')(player_data,
                                                             self.edit_mode)
        if success:
            messagebox.showinfo("Succès", message)
            for entry in self.entries.values():
                entry.delete(0,
                             tk.END)
            self.load_players()
            self.reset_form()
            self.notebook.select(1)
        else:
            messagebox.showerror("Erreur", message)

    def handle_click(self, event):
        """Handle click events on the players table"""
        region = self.players_table.identify_region(event.x,
                                                    event.y)
        if region == "cell":
            item = self.players_table.selection()[0]
            column = self.players_table.identify_column(event.x)
            if column == '#5':
                values = self.players_table.item(item)['values']
                self.fill_edit_form(values)

    def fill_edit_form(self, values):
        """Fill the add player form with existing values for editing"""
        fields = ["national_id",
                  "last_name",
                  "first_name",
                  "birth_date"]

        self.original_id = values[0]

        for field, value in zip(fields,
                                values):
            self.entries[field].delete(0,
                                       tk.END)
            self.entries[field].insert(0,
                                       value)

        self.edit_mode = True
        self.notebook.select(0)

    def load_players(self):
        """Load and display all players in the table"""
        for item in self.players_table.get_children():
            self.players_table.delete(item)

        players = self.callbacks.get('load_players')()
        for national_id, player_data in players.items():
            self.players_table.insert(
                "",
                tk.END,
                values=(
                    national_id,
                    player_data["last_name"],
                    player_data["first_name"],
                    player_data["birth_date"],
                    "✏️"  # Edit icon
                )
            )

    def reset_form(self):
        """Reset the form to its initial state"""
        for entry in self.entries.values():
            entry.delete(0,
                         tk.END)
            self.edit_mode = False
            self.original_id = None
