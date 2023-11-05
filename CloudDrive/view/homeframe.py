import os
from dotenv import load_dotenv
from logic.cloud import CloudSetup
from logic.homelogic import HomeLogic
import tkinter as tk
import customtkinter as ctk
from PIL import Image
load_dotenv(".env")

class HomeFrame():
    """
        This class defines the Home frame. Home frame is the frame 
        shown to the user after successfull authentication. 
        How this frame looks?
        - It has a sidebar on the left side of the frame,
        which contains the user details and the cloud provider details,
        And has the upload button.
        - It has a main content area in the middle of the frame (covers 80% of the frame),
        which contains the files and folders of the user.
        - parent: the parent of the frame
    """
    def __init__(self, parent, prev, userObj):
        """
            This is the constructor of the HomeFrame class.
            - parent: the parent of the frame
            - prev: the previous frame
            - userObj: the user object, which contains the user details
        """
        # Initialize HomeLogic class
        self.homeLogic = HomeLogic(userObj)
        # Initialize the frame
        self.remove_frame(prev)
        self.parent = parent
        self.frame = prev
        self.userObj = userObj
        self.frame.grid(row=0, column=0)
        self.frame.pack_propagate(False)
        self.frame.tkraise()
        self.build()


    def build(self):
        """
            build() method builds the Home frame.
        """
        self.frame.configure(fg_color=os.getenv("HOME_SCREEN_BG_COLOR"), corner_radius=0)
        self.build_sidebar()
        self.build_main_content()


    def build_sidebar(self):
        """
            build_sidebar() method builds the sidebar of the Home frame.
            This sidebar contains the My Account tab and Upload button.
        """
        # Left Sidebar
        self.left_sidebar = ctk.CTkFrame(self.frame,
            width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.2,
            height=int(os.getenv("DEFAULT_APP_HEIGHT")),
            fg_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            corner_radius=0
        )

        """
            Left Sidebar Content
            - App Title Logo
            - Upload Button
            - My Account
        """
        # App Title Logo
        cloud_img = ctk.CTkImage(Image.open(os.getenv("CLOUD_ICON")), size=(45, 45))
        ctk.CTkButton(master=self.left_sidebar,
            image=cloud_img,
            fg_color="transparent",
            hover=False,
            text=os.getenv("APP_TITLE"),
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT4_SIZE"), 12)),
            text_color=os.getenv("WHITE_COLOR")
        ).pack(pady=60, side=tk.TOP, padx=10)

        # Upload Button
        upload_img = ctk.CTkImage(Image.open(os.getenv("UPLOAD_ICON")), size=(int(os.getenv("DEFAULT_ICON_SIZE")), int(os.getenv("DEFAULT_ICON_SIZE"))))
        ctk.CTkButton(self.left_sidebar,
            text="Upload",
            image=upload_img,
            height=35,
            text_color=os.getenv("WHITE_COLOR"),
            fg_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            hover_color="#0077B6",
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 15)),
            command=lambda: self.homeLogic.launch_file_explorer()
        ).pack(padx=10, pady=20)

        # My Account
        self.my_account = ctk.CTkFrame(self.left_sidebar,
            width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.18,
            height=int(os.getenv("DEFAULT_APP_HEIGHT"))*0.1,
            fg_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            corner_radius=10
        )
        self.my_account.pack_propagate(False)
        self.my_account.pack(side=tk.BOTTOM, pady=10)
        self.my_account.tkraise()

        # My Account Label
        user_icon_img = ctk.CTkImage(Image.open(os.getenv("USER_ICON")), size=(int(os.getenv("DEFAULT_ICON_SIZE")), int(os.getenv("DEFAULT_ICON_SIZE"))))
        ctk.CTkButton(self.my_account,
            text="My Account",
            image=user_icon_img,
            text_color=os.getenv("WHITE_COLOR"),
            fg_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            hover_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 12)),
            command=lambda: ()
        ).pack(padx=10)

        self.left_sidebar.pack_propagate(False)
        self.left_sidebar.pack(side=tk.LEFT, pady=10, padx=10)
        self.left_sidebar.tkraise()


    def build_main_content(self):
        """
            build_main_content() method builds the main content of the Home frame.
            This main content contains the uploaded files and folders of the user.
        """
        # Main Content
        self.main_content = ctk.CTkFrame(self.frame,
            width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.8,
            height=int(os.getenv("DEFAULT_APP_HEIGHT")),
            fg_color="#f7fcfe",
            corner_radius=25
        )

        ctk.CTkLabel(self.main_content,
            text="My Cloud",
            fg_color="#f7fcfe",
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT4_SIZE"), 12))
        ).pack(pady=30, padx=30, side=tk.TOP, anchor=tk.W)

        ctk.CTkLabel(self.main_content,
            text="Hi "+self.userObj["username"]+", Welcome to your CloudDrive!",
            fg_color="#f7fcfe",
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 12))
        ).pack(pady=0, padx=30, side=tk.TOP, anchor=tk.W)

        # Main Content - Files (grid view)
        self.files = ctk.CTkScrollableFrame(master=self.main_content,
            width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.8,
            height=int(os.getenv("DEFAULT_APP_HEIGHT"))*0.7,
            fg_color="#ffffff",
            corner_radius=25
        )
        # populate files
        self.homeLogic.populate_files(self.files)

        # configure the grid
        self.files.pack(side=tk.TOP, pady=10, padx=10)
        self.files.pack_propagate(False)

        # configure the main content
        self.main_content.pack(side=tk.RIGHT, pady=10, padx=10)
        self.main_content.tkraise()


    def remove_frame(self, frame):
        """
            remove_frame() method removes the current frame
        """
        for widget in frame.winfo_children():
            widget.destroy()
