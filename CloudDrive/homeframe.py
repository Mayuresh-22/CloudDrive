import tkinter as tk
import customtkinter as ctk

class HomeFrame():
    # create a hello world button
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.pack_propagate(False)
        self.frame.tkraise()
        self.hello_world_button = ctk.CTkButton(self.frame, 
                                                text="Hello World! Home Page", 
                                                command=lambda: self.hello_world())
        self.hello_world_button.pack(padx=50, pady=50)

    
    def hello_world(self):
        print("Hello World! Home Page")
