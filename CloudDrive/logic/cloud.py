"""
    This file contains the logic for the cloud cloud provider setup.
"""
from re import T
from tkinter import filedialog
from filestack import Client
import os
from dotenv import load_dotenv
import requests
from homelogic import HomeLogic
load_dotenv(".env")

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
        self.cloud_provider = cloud_provider
        self.api_key = api_key
        self.kwargs = kwargs

    def setup(self, **kwargs):
        """
            This method return the cloud provider object.
        """
        if self.cloud_provider == os.getenv("FILESTACK"):
            return Filestack(self.api_key, **self.kwargs)
        else:
            return None
        

class Filestack():
    """
        This class contains the logic for the Filestack cloud provider setup and actions.
        It inherits the CloudSetup class.
        
        This class has the following methods:
        - filestack_setup(): This method setups the Filestack cloud provider.
        - upload_file(): This method uploads the file to the cloud and returns the file link,
                        which contains the file details.
    """
    def __init__(self, api_key, **kwargs):
        """
            This is the constructor of the Filestack class.
            - cloudSetObj: the cloud provider setup object (CloudSetup)
        """
        self.api_key = api_key
        self.filelink = None
        self.filetypes = {
            "pdf" : ("PDF files","*.pdf"),
            "docx" : ("DOCX files","*.docx"),
            "png" : ("PNG files","*.png"),
            "jpg" : ("JPEG files","*.jpg"),
            "jpeg" : ("JPEG files","*.jpeg"),
            "txt" : ("Text files","*.txt"),
            "all" : ("All files","*.*")
        }
        

    def setup(self, **kwargs) -> None:
        """
            This method setups the Filestack cloud provider.
        """
        # Initialize the Filestack Setup
        self.client = Client(self.api_key)
        # print("Filestack setup done")


    def upload_file(self, file, files_frame):
        """
            This method uploads the file to the cloud.
            - file: the file to be uploaded
            - file_frame: the frame where uploaded files are populated
        """
        self.filelink = self.client.upload(filepath=file)

                # Checking if the file is uploaded successfully
        if self.filelink.upload_response["status"] == "Stored":
            """
                If the file is uploaded successfully,
                Now, storing the file details in the database.
            """
            url = os.getenv("APP_BASE_URL")+os.getenv("FILE_ENDPOINT")+os.getenv("UPLOAD_ENDPOINT")
            resp = requests.post(url,
                headers={"Content-Type": "application/json"},
                json={
                    "file_owner" : self.userObj["id"],
                    "cloud_provider_api_key" : self.userObj["cloud_provider_api_key"],
                    "file_name" : self.filelink.upload_response["filename"],
                    "file_size" : self.filelink.upload_response["size"],
                    "file_type" : self.filelink.upload_response["mimetype"],
                    "file_url_pub" : self.filelink.upload_response["url"],
                    "file_url_pvt" : "",
                    "file_handle" : self.filelink.upload_response["handle"],
                    "file_status" : self.filelink.upload_response["status"]
                }
            )
            if resp.status_code == 200 and resp.json()["status"] == "success":
                # print(resp.json()["message"])
                HomeLogic.populate_files(files_frame)
            else:
                # print(resp.json()["message"])
                pass
    

    def download_file(self, fileurl, filename):
        """
            This method downloads the file from the cloud.
            It sends the GET request to the file url and downloads the file.
            - fileurl: the file url to be downloaded
        """
        print("Downloading...")
        file_type = filename.split(".")[-1]

        # send the GET request to the file url
        resp = requests.get(fileurl)

        # write the response content to the file
        new_filename =  filedialog.asksaveasfilename(initialdir="/Downloads", title="Save file",
            filetypes=((file_type, f"*.{file_type}"),("All files", "*.*")))
        
        # if the user cancels the save file dialog
        if new_filename == "":
            return False
        
        with open(f"{new_filename}.{file_type}", "wb") as f:
            f.write(resp.content)

        return True
    
