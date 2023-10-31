"""
    HomeLogic is rhe class that handles the logic for the home page.
"""

from tkinter import filedialog


class HomeLogic:
    """
        This class handles the logic behind the Home fram (after successfull authentication).
    """
    def launch_file_explorer():
        """
            This method launches the file explorer of the system.
            Opens the file dialog to select the file.
        """
        file = filedialog.askopenfilename(initialdir="/", title="Select a File")
        
        if file:
            print(file)
