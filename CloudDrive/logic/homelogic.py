"""
    HomeLogic is rhe class that handles the logic for the home page.
"""

# Import the required modules
import os
from dotenv import load_dotenv
from tkinter import filedialog
from functools import partial
from PIL import Image
import requests
from logic.cloud import CloudSetup
import customtkinter as ctk
import tkinter as tk
import threading

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

        # Set the file icons
        file_icons_theme = os.getenv("FILE_ICON_PLAIN")
        if file_icons_theme == os.getenv("FILE_ICON_PLAIN"):
            self.file_icons = {
                "pdf" : os.getenv("PDF_ICON_PLAIN"),
                "octet-stream" : os.getenv("DOC_ICON_PLAIN"),
                "png" : os.getenv("IMAGE_ICON_PLAIN"),
                "jpg" : os.getenv("IMAGE_ICON_PLAIN"),
                "jpeg" : os.getenv("IMAGE_ICON_PLAIN"),
                "plain" : os.getenv("TXT_ICON_PLAIN")
            }
        elif file_icons_theme == os.getenv("FILE_ICON_3D"):
            self.file_icons = {
                "pdf" : os.getenv("PDF_ICON_3D"),
                "octet-stream" : os.getenv("DOC_ICON_3D"),
                "png" : os.getenv("IMAGE_ICON_3D"),
                "jpg" : os.getenv("IMAGE_ICON_3D"),
                "jpeg" : os.getenv("IMAGE_ICON_3D"),
                "plain" : os.getenv("TXT_ICON_3D")
            }
        elif file_icons_theme == os.getenv("FILE_ICON_MED"):
            self.file_icons = {
                "pdf" : os.getenv("PDF_ICON_MED"),
                "octet-stream" : os.getenv("DOC_ICON_MED"),
                "png" : os.getenv("PNG_ICON_MED"),
                "jpg" : os.getenv("JPG_ICON_MED"),
                "jpeg" : os.getenv("JPEG_ICON_MED"),
                "plain" : os.getenv("TXT_ICON_MED")
            }
        

    def launch_file_explorer(self, files_frame) -> None:
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
            self.upload_file(file, files_frame)


    def upload_file(self, file, files_frame):
        """
            This method is the global method to upload the file to the cloud.
            - file: the file to be uploaded

            This method calls the upload_file() method of the respective cloud provider.
        """

        # Calling the upload_file() method of the respective cloud provider
        # start the thread to upload the file
        thread = threading.Thread(target=self.cloud.upload_file, args=(file, files_frame))
        thread.start()
        
        
    def download_file(self, file_url, file_name):
        """
            This method downloads the file from the cloud.
            This method call the download_file() method of the respective cloud provider.
        """
        # calling the download_file() method of the respective cloud provider
        bool = self.cloud.download_file(file_url, file_name)

