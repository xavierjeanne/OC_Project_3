from tkinter import ttk


class RoundView(ttk.Frame):
    """View for managing chess rounds,
    including creation and management of rounds"""

    def __init__(self, parent, **callbacks):
        """Initialize the round management view

        Args:
            parent: Parent widget containing this view
            callbacks: Dictionary containing
            callback functions for round operations
        """
        super().__init__(parent, style='Main.TFrame')
        self.callbacks = callbacks
        self.edit_mode = False
        # Return button
        ttk.Button(self,
                   text="Retour à l'accueil",
                   command=self.callbacks.get('return_home'),
                   cursor='hand2',
                   style='Custom.TButton').grid(row=0, column=0, pady=10)

        # Create notebook
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Create round tab
        self.add_round_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.add_round_frame, text="Generer un tour")
        self._setup_add_round_tab()

        # round list tab
        self.list_rounds_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.list_rounds_frame, text="Liste des tours")
        self._setup_list_rounds_tab()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _setup_add_round_tab(self):
        """Set up the tab for creating new rounds

        adds a form with fields for:
        - round name
        """
        pass

    def _setup_list_rounds_tab(self):
        """Set up the tab for displaying and managing rounds

        Features:
        - round list table
        """
        pass
