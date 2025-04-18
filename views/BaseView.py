from tkinter import ttk
from PIL import Image, ImageTk
from utils.StyleConfig import StyleConfig


class BaseView:
    """Base view class that sets up the main application window structure and styling"""

    def __init__(self, master):
        """Initialize the base view with main frame and logo

        Args:
            master: The root window or parent widget

        Features:
            - Configures application styles
            - Sets up responsive grid layout
            - Loads and displays chess logo
            - Creates content container for child views
        """

        self.master = master
        StyleConfig.configure_styles()

        # Configure grid weights
        self.master.grid_rowconfigure(0,
                                      weight=1)
        self.master.grid_columnconfigure(0,
                                         weight=1)
        # Create main frame
        self.frame = ttk.Frame(self.master,
                               style='Main.TFrame')
        self.frame.grid(row=0,
                        column=0,
                        sticky="nsew")

        # Configure grid weights
        self.frame.grid_rowconfigure(0,
                                     weight=0)
        self.frame.grid_rowconfigure(1,
                                     weight=1)
        self.frame.grid_columnconfigure(0,
                                        weight=1)

        try:
            image = Image.open(
                "assets/chess_logo.png"
                )
            image = image.resize((200, 200))
            self.photo = ImageTk.PhotoImage(image)  # Store as an instance attribute
            self.image_label = ttk.Label(self.frame,
                                         image=self.photo,
                                         background='#2C3E50')
            self.image_label.grid(row=0,
                                  column=0,
                                  pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Create a placeholder if image fails to load
            placeholder = ttk.Label(self.frame,
                                    text="[Chess Logo]",
                                    font=("Helvetica", 14),
                                    background='#2C3E50',
                                    foreground="white")
            placeholder.grid(row=1,
                             column=0,
                             pady=20)

        # Content container for child views
        self.content_container = ttk.Frame(self.frame,
                                           style='Main.TFrame')
        self.content_container.grid(row=1,
                                    column=0,
                                    sticky="nsew",
                                    padx=20,
                                    pady=20)

        self.content_container.grid_rowconfigure(0,
                                                 weight=1)
        self.content_container.grid_columnconfigure(0,
                                                    weight=1)
