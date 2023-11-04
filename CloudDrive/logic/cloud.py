"""
    This file contains the logic for the cloud cloud provider setup.
"""
import json
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

        if self.cloud_provider == os.getenv(os.getenv("FILESTACK")):
            self.filestack_setup()
        else:
            pass
    

class Filestack(CloudSetup):
    """
        This class contains the logic for the Filestack cloud provider setup and actions.
    """

    def filestack_setup(self, **kwargs) -> None:
        # Initialize the Filestack Setup
        self.client = Client(self.api_key)
        print("Filestack setup done")


    def upload_file(self, file):
        """
            This method uploads the file to the cloud.
            - file: the file to be uploaded
        """
        filelink = self.client.upload(filepath=file)
        return filelink
