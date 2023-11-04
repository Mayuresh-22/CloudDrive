"""
    This file contains the logic for the cloud cloud provider setup.
"""
from filestack import Client, Security
import time

class CloudSetup():
    """
        This class contains the logic for the cloud cloud provider setup.
    """
    def __init__(self, cloud_provider, api_key):
        """
            This is the constructor for the class.
            Checks the cloud provider and calls the respective method.
        """