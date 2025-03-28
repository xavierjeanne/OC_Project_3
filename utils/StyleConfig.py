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
                        foreground='white',
                        padding=5,
                        borderwidth=0)

        # Notebook tab style
        style.configure('Custom.TNotebook.Tab',
                        background='#2C3E50',
                        foreground='#2C3E50',
                        padding=[10, 5],
                        font=('Helvetica', 10, 'bold'))
