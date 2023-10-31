"""
    HomeLogic is rhe class that handles the logic for the home page.
"""

import os


class HomeLogic:
    """
        This class handles the logic behind the Home fram (after successfull authentication).
    """
    def launch_file_explorer():
        """
            This method launches the file explorer of the system.
        """
        os.system("xdg-open "+os.getenv("DEFAULT_APP_DOWNLOAD_PATH"))
        
