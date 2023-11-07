"""
    This file is the main file of the CloudDrive App.
"""

# import modules
from view.authframe import AuthFrame
import os
import customtkinter as ctk
from dotenv import load_dotenv
load_dotenv(".env")


class App:
    """
        This class is the main class of the CloudDrive App.
        - root: the root of the app
        - app_config: the method to set the config of the app
        - __init__: the constructor of the App class
    """
    def __init__(self):
        """
            This is the constructor of the App class.
        """
        self.root = ctk.CTk()
        self.root.title(os.getenv("APP_TITLE"))

        self.root.geometry(f"{os.getenv('DEFAULT_APP_WIDTH')}x{os.getenv('DEFAULT_APP_HEIGHT')}")
        self.root.resizable(False, False)
        self.root.iconbitmap(os.getenv("APP_ICON"))
        # Build the Auth frame
        AuthFrame(self.root)
        self.root.mainloop()
    
    
    def app_config(self):
        """
            This method is used to set the theme of the app.
        """
        ctk.set_appearance_mode(os.getenv("DEFAULT_APPEARANCE_MODE"))
        ctk.set_default_color_theme(os.getenv("DEFAULT_COLOR_THEME"))


if __name__ == "__main__":
    app = App()
    