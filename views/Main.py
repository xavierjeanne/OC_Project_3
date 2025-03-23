import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess Tournament Manager")
        self.root.geometry("400x400")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame with matching background
        style = ttk.Style()
        style.configure('Main.TFrame', background='#2C3E50')
        self.main_frame = ttk.Frame(self.root, padding="10", style='Main.TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Configure main frame grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Add image
        image = Image.open("c:/Users/xavie/Documents/OC_Project_3/assets/chess_logo.png")
        image = image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label = ttk.Label(self.main_frame, image=self.photo)
        self.image_label.grid(row=0, column=0, pady=10)
        
        # Create buttons
        ttk.Button(self.main_frame, text="Add a player", command=self.root.quit).grid(row=1, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(self.main_frame, text="Create a tournament", command=self.root.quit).grid(row=2, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(self.main_frame, text="Load a tournament", command=self.root.quit).grid(row=3, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(self.main_frame, text="Exit", command=self.root.quit).grid(row=4, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        
    def add_player(self):
        print("Add player clicked")
        
    def create_tournament(self):
        print("Create tournament clicked")
        
    def load_tournament(self):
        print("Load tournament clicked")

    def run(self):
        self.root.mainloop()