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
            - cloud_provider: the cloud provider of the user
            - api_key: the api key of the user
        """
        self.cloud_provider = cloud_provider
        self.api_key = api_key

    def upload_file(self, filepath):
        """
            This method uploads the file to the cloud provider.
            - filepath: the path of the file to be uploaded
        """
        # Initialize the client
        client = Client(self.api_key)

        # Get the current time in seconds since the Unix epoch
        now = int(time.time())

        # Add one hour in seconds to the current time
        expiration_time = now + 3600

        policy = {
            "expiry": expiration_time, 
            "call": ["pick","read","stat","write","store","convert","remove","exif","writeUrl","runWorkflow"]
        }
        security = Security(policy, "7PDJLJSTP5G33M7FKQQE3Q4W3E")

        fileinfo = client.upload(filepath=filepath, security=security)
        # print(fileinfo.upload_response)
        return f"https://cdn.filestackcontent.com/{security.as_url_string()}/{fileinfo.upload_response['handle']}"