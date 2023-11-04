"""
    HomeLogic is rhe class that handles the logic for the home page.
"""

# Import the required modules
import os
from dotenv import load_dotenv
from tkinter import filedialog
import requests
from logic.cloud import CloudSetup, Filestack

load_dotenv(".env")

class HomeLogic:
    """
        HomeLogic is the class that handles the logic for the home page.
        This class __init__ method takes the user object as the parameter.
        This class has the following methods:
        - launch_file_explorer(): This method launches the file explorer of the system.
        - upload_file(): This method is the global method to upload the file to the cloud.

        This class has the following attributes:
        - userObj: the user object, which contains the user details (JSON)
        - cloud: the cloud provider setup object (CloudSetup)
        - filehandler: the file handler object for the cloud provider,
                    which handles the file actions (Any cloud provider type)

    """
    def __init__(self, userObj):
        """
            This is the constructor of the HomeLogic class.
            - userObj: the user object, which contains the user details
        """
        self.userObj = userObj
        self.cloud = CloudSetup(userObj["cloud_provider"], userObj["cloud_provider_api_key"]).setup()

        if self.cloud != None:
            self.cloud.setup()


    def launch_file_explorer(self) -> None:
        """
            This method launches the file explorer of the system.
            Opens the file dialog to select the file.
        """
        file = filedialog.askopenfilename(initialdir="/", filetypes=[("Text file", "*.txt"), ("PDF file", "*.pdf"),  ("Docx file", "*.docx"), ("Image file", "*.png *jpg")], title="Select a File to Upload")
        
        if file:
            """
                If the file is selected,
                This method calls the global method upload_file() to upload the file to the cloud.
            """
            self.upload_file(file)


    def upload_file(self, file):
        """
            This method is the global method to upload the file to the cloud.
            - file: the file to be uploaded

            This method calls the upload_file() method of the respective cloud provider.
        """
        filelink = self.cloud.upload_file(file)
        
        if filelink.upload_response["status"] == "Stored":
            """
                If the file is uploaded successfully,
                Now, storing the file details in the database.
            """
            url = os.getenv("APP_BASE_URL")+os.getenv("FILE_ENDPOINT")+os.getenv("UPLOAD_ENDPOINT")
            try:
                resp = requests.post(url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "file_owner" = filelink.upload_response["file_owner"],
                        "file_name" = filelink.upload_response["file_name"],
                        "file_size" = filelink.upload_response["file_size"],
                        "file_type" = filelink.upload_response["file_type"],
                        "file_url_pub" = filelink.upload_response["file_url_pub"],
                        "file_url_pvt" = filelink.upload_response["file_url_pvt"],
                        "file_url_pub" = filelink.upload_response["file_url_pub"],
                        "file_url_pub" = filelink.upload_response["file_url_pub"],
                    }
                    
                )
            except:
                pass