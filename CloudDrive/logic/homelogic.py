"""
    HomeLogic is rhe class that handles the logic for the home page.
"""

# Import the required modules
import os
from dotenv import load_dotenv
from logic.cloud import CloudSetup
from view.accountframe import AccountFrame
from tkinter import filedialog
from functools import lru_cache, partial
from PIL import Image
from functools import partial, lru_cache
import requests
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
        self.progress = None
        self.cloud = CloudSetup(userObj["cloud_provider"], userObj["cloud_provider_api_key"]).setup()
        if self.cloud != None:
            self.cloud.setup()

        # Set the file icons
        file_icons_theme = os.getenv("FILE_ICON_3D")
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

 
    @lru_cache
    def launch_file_explorer(self, files_frame, progress) -> None:
        """
            This method launches the file explorer of the system.
            Opens the file dialog to select the file.
        """
        self.progress = progress
        file = filedialog.askopenfilename(initialdir="/", filetypes=[("Text file", "*.txt"), ("PDF file", "*.pdf"),  ("Docx file", "*.docx"), ("Image file", "*.png *jpg")], title="Select a File to Upload")
        
        if file:
            """
                If the file is selected,
                This method calls the global method upload_file() to upload the file to the cloud.
            """
            self.progress.configure(text="Uploading file...")
            # start the thread to upload the file
            threading.Thread(target=self.upload_file, args=(file, files_frame)).start() 


    def populate_files(self, files_frame):
        """
            This method populates the files in the files frame.
            - files_frame: the frame to populate the files

            This method sends POST request to the server to get the files of the user.
            and populates the files in the files frame.
    """
        
        # Clear the files frame
        for widget in files_frame.winfo_children():
            widget.destroy()

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
                user_files_list = resp.json()["files"]
                if len(user_files_list) == 0:
                    no_file_label = ctk.CTkLabel(files_frame,
                        text="No files found",
                        text_color=os.getenv("PRIMARY_COLOR_MED"),
                        font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT5_SIZE"), 12))
                    )
                    no_file_label.grid(row=0, column=0, rowspan=4, columnspan=4, padx=10, pady=10)
                    no_file_label.pack_propagate(False)
                    no_file_label.grid_propagate(False)
                    return
                
                row = 0
                col = 0
                max_col = 4
                for file in user_files_list[::-1]:
                    file_type = file["file_type"].split("/")[1]
                    """
                        Creating the file block
                        File block contains the file icon and the file name
                        And, action buttons to download, view, delete the file
                    """
                    file_block = ctk.CTkFrame(files_frame,
                        width=190,
                        height=190,
                        fg_color="#E3F5FD",
                        corner_radius=10
                    )
                    file_block.grid(row=row, column=col, padx=10, pady=10)
                    file_block.pack_propagate(False)
                    file_block.grid_propagate(False)

                    # file icon
                    file_icon = ctk.CTkImage(Image.open(self.file_icons[file_type]), size=(55, 55))
                    ctk.CTkLabel(file_block,
                        image=file_icon,
                        text="",
                        fg_color="#E3F5FD",
                        bg_color="#E3F5FD",
                    ).pack(pady=20, side = tk.TOP)

                    # file name
                    file_name = ctk.CTkLabel(file_block,
                        text=file["file_name"][0:15]+"...",
                        fg_color="#E3F5FD",
                        text_color="#1B387C",
                        font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 10))
                    )
                    file_name.pack(pady=5)

                    # file actions
                    file_actions = ctk.CTkFrame(file_block,
                        width=190,
                        height=30,
                        fg_color="#E3F5FD",
                        corner_radius=10
                    )
                    file_actions.pack(pady=10)
                    file_actions.pack_propagate(False)

                    # download button
                    download_icon = ctk.CTkImage(Image.open(os.getenv("DOWNLOAD_ICON")), size=(30, 30))
                    download_button = ctk.CTkButton(file_actions,
                        width=50,
                        image=download_icon,
                        text="",
                        fg_color="transparent",
                        bg_color="transparent",
                        hover=False,
                        font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 10)),
                        command=partial(self.download_file, file["file_url"], file["file_name"])
                    )
                    download_button.pack(side=tk.LEFT, padx=5)

                    col += 1
                    if col == max_col:
                        row += 1
                        col = 0
        except Exception as e:
            print(e)


    def upload_file(self, file, files_frame) -> None:
        """
            This method is the global method to upload the file to the cloud.
            - file: the file to be uploaded

            This method calls the upload_file() method of the respective cloud provider.
            then filelink object is used to store the file details in the database.
        """
        # check if the file already exists for the user
        url = os.getenv("APP_BASE_URL")+os.getenv("FILE_ENDPOINT")+os.getenv("UPLOAD_ENDPOINT")+"check/"
        resp = requests.post(url,
            headers={"Content-Type": "application/json"},
            json={
                "file_owner" : self.userObj["id"],
                "file_name" : os.path.basename(file)
            }
        )
        if resp.status_code == 200 and resp.json()["status"] == "success":
            if resp.json()["file_exists"] == "True":
                print("File already exists...Duplicate")
                self.progress.configure(text=resp.json()["message"])
                return
        # upload the file to the cloud by calling the upload_file() method of the respective cloud provider
        filelink = self.cloud.upload_file(file)
        
        # Checking if the file is uploaded successfully
        if filelink.upload_response["status"] == "Stored" and filelink is not None:
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
                self.populate_files(files_frame)
                self.progress.configure(text=resp.json()["message"])

        
    def download_file(self, file_url, file_name):
        """
            This method downloads the file from the cloud.
            This method call the download_file() method of the respective cloud provider.

            - file_url: URL of the file to be downloaded
            - file_name: name of the file to be downloaded
        """
        threading.Thread(target=self.cloud.download_file, args=(file_url, file_name)).start()


    def load_account_frame(self, parent, current, userobj):
        # load Account Frame
        AccountFrame(parent, current, userobj).build()
