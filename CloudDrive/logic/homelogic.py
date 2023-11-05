"""
    HomeLogic is rhe class that handles the logic for the home page.
"""

# Import the required modules
import os
from urllib import response
from dotenv import load_dotenv
from tkinter import filedialog
import requests
from logic.cloud import CloudSetup, Filestack
import customtkinter as ctk

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
            resp = requests.post(url,
                headers={"Content-Type": "application/json"},
                json={
                    "file_owner" : self.userObj["id"],
                    "cloud_provider_api_key" : self.userObj["cloud_provider_api_key"],
                    "file_name" : filelink.upload_response["filename"],
                    "file_size" : filelink.upload_response["size"],
                    "file_type" : filelink.upload_response["mimetype"],
                    "file_url_pub" : filelink.upload_response["url"],
                    "file_url_pvt" : "",
                    "file_handle" : filelink.upload_response["handle"],
                    "file_status" : filelink.upload_response["status"]
                }
            )
            if resp.status_code == 200 and resp.json()["status"] == "success":
                print(resp.json()["message"])
            else:
                print(resp.json()["message"])

    def populate_files(self, files_frame):
        """
            This method populates the files in the files frame.
            - files_frame: the frame to populate the files

            This method sends POST request to the server to get the files of the user.
            and populates the files in the files frame.
    """
        # Get the files from the server for the user
        url = os.getenv("APP_BASE_URL")+os.getenv("FILE_ENDPOINT")
        try:
            resp = requests.post(url,
                headers={"Content-Type": "application/json"},
                json={
                    "file_owner" : self.userObj["id"],
                    "cloud_provider_api_key" : self.userObj["cloud_provider_api_key"]
                }
            )
            if resp.status_code == 200 and resp.json()["status"] == "success":
                files = resp.json()["files"]
                for file in files:
                    file_frame = ctk.CTkFrame(files_frame,
                        width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.8,
                        height=50,
                        fg_color="#E3F5FD",
                        corner_radius=10
                    )

                    file_frame.pack(pady=5)
                    file_frame.pack_propagate(False)
                    file_frame.grid_propagate(False)
   
        except Exception as e:
            print(e)
