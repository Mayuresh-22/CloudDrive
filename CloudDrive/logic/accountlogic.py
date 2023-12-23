"""
    AccountLogic class is used to implement user Account Frame logic,
    And handles the routing between Account & Home Frame.
"""
import os
from dotenv import load_dotenv
from view.homeframe import HomeFrame

class AccountLogic:
    """
        This class handels the logic behind the Account Frame
        Displaying user information and modifying it.
    """
    def load_home_frame(self, parent, current, userobj):
        """
            This method is used to load the Home Frame
            and pass the user object to it.
        """
        HomeFrame(parent, current, userobj).build()
