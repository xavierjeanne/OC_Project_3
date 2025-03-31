from tkinter import ttk


class StyleConfig:
    """Configures the visual styles for the application's UI components"""

    @staticmethod
    def configure_styles():
        """Configure ttk styles for various UI elements

        Defines styles for:
        - Main frame (Main.TFrame)
        - Custom buttons (Custom.TButton)
        - Notebook and tabs (Custom.TNotebook)

        Color scheme:
        - Primary: #2C3E50 (Dark blue)
        - Text: white
        """
        style = ttk.Style()

        # Main frame style
        style.configure('Main.TFrame', background='#2C3E50')

        # Button style
        style.configure('Custom.TButton',
                        background='#2C3E50',
                        foreground='#2C3E50',
                        font=('Helvetica', 12, 'bold'),
                        padding=15)

        style.map('Custom.TButton',
                  background=[('active', '#2C3E50')],
                  foreground=[('active', '#2C3E50')])

        # Notebook style
        style.configure('Custom.TNotebook',
                        background='#2C3E50',
                        padding=0,
                        borderwidth=0,
                        relief='flat',
                        tabmargins=[0, 0, 0, 0],
                        tabposition='n'
                        )

        # Notebook tab style
        style.configure('Custom.TNotebook.Tab',
                        foreground='#2C3E50',
                        borderwidth=0,
                        padding=[10, 5],
                        font=('Helvetica', 10, 'bold'))

        # Treeview style
        style.configure('Custom.Treeview',
                        background='#34495E',
                        foreground='white',
                        fieldbackground='#34495E',
                        borderwidth=0)

        style.configure('Custom.Treeview.Heading',
                        background='#2C3E50',
                        foreground='#2C3E50',
                        relief='flat',
                        borderwidth=0,
                        anchor='n'
                        )

        style.map('Custom.Treeview',
                  background=[('selected', '#1ABC9C')],
                  foreground=[('selected', 'white')])

        style.configure('Custom.TLabel',
                        background='#2C3E50',
                        foreground='white',
                        font=('Helvetica', 12, 'bold')
                        )
