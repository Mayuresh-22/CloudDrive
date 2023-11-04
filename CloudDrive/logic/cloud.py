"""
    This file contains the logic for the cloud cloud provider setup.
"""
from filestack import Client, Security
import os
from dotenv import load_dotenv
load_dotenv(".env")
import time

class CloudSetup():
    """
        This class contains the logic for the cloud cloud provider setup.
    """

    def __init__(self, cloud_provider, api_key, **kwargs):
        """
            This is the constructor for the class.
            Checks the cloud provider and calls the respective method.
        """
        self.client = None
        self.cloud_provider = cloud_provider
        self.api_key = api_key
        self.kwargs = kwargs

        if self.cloud_provider == "Filestack":
            self.filestack_setup()
        else:
            pass
    
    def filestack_setup(self, **kwargs):
        # Initialize the Filestack Setup
        self.client = Client(self.api_key)
        print("Filestack setup done")


