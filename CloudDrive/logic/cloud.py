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
        This class contains the logic for the cloud provider setup and actions.
        __init__ method takes the cloud provider and the api key as the parameters.
        This class setups the cloud provider of the user.
    """

    def __init__(self, cloud_provider, api_key, **kwargs):
        """
            This is the constructor for the class.
            Checks the cloud provider and calls the respective method.
        """
        client = None
        cloud_provider = cloud_provider
        api_key = api_key
        kwargs = kwargs

        if cloud_provider == os.getenv(os.getenv("FILESTACK")):
            Filestack.filestack_setup(Filestack)
        else:
            pass
    

class Filestack(CloudSetup):
    """
        This class contains the logic for the Filestack cloud provider setup and actions.
        It inherits the CloudSetup class.
        
        This class has the following methods:
        - filestack_setup(): This method setups the Filestack cloud provider.
        - upload_file(): This method uploads the file to the cloud and returns the file link,
                        which contains the file details.
    """
    def __init__(self, **kwargs):
        super().__init__(self, cloud_provider="Filestack", api_key="1233")


    def main(self):
        print("Filestack main")
        # PRINT cloudsetup class attributes
        print(self.client)
        print(self.cloud_provider)

    # def filestack_setup(self, **kwargs) -> None:
    #     # Initialize the Filestack Setup
    #     self.client = Client(self.api_key)
    #     print("Filestack setup done")


    # def upload_file(self, file):
    #     """
    #         This method uploads the file to the cloud.
    #         - file: the file to be uploaded
    #     """
    #     filelink = self.client.upload(filepath=file)
    #     return filelink


if __name__ == "__main__":
    file = Filestack()
    file.main()