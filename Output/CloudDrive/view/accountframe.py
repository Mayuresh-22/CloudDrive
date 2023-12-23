import os
from dotenv import load_dotenv
import tkinter as tk
import customtkinter as ctk
from PIL import Image

load_dotenv(".env")

class AccountFrame():
    """
        This class defines the account frame. Account frame is the frame
        shown to the user after he/she clicks on the My Account button.
        
        How this frame looks?
        - It has a sidebar on the left side of the frame,
        which the home button at the bottom of the sidebar.
        - It has a main content area in the middle of the frame (covers 80% of the frame),
        which contains the user details.
        
        Args:
        - parent: the parent of the frame
        - prev: the previous frame
        - userObj: the user object, which contains the user details
    """
    def __init__(self, parent, prev, userObj):
        
        """
            This is the constructor of the AccountFrame class.
            - parent: the parent of the frame
            - prev: the previous frame
            - userObj: the user object, which contains the user details
        """
        # Initialize AccountLogic Class
        from logic.accountlogic import AccountLogic
        self.accountlogic = AccountLogic()
        # Initialize the frame
        self.remove_frame(prev)
        self.parent = parent
        self.frame = prev
        self.userObj = userObj
        self.frame.grid(row=0, column=0)
        self.frame.pack_propagate(False)
        self.frame.tkraise()


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
            - Home Button
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
                                        
        # Home Button
        self.home_btn = ctk.CTkFrame(self.left_sidebar,
            width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.18,
            height=int(os.getenv("DEFAULT_APP_HEIGHT"))*0.1,
            fg_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            corner_radius=10
        )
        self.home_btn.pack_propagate(False)
        self.home_btn.pack(side=tk.BOTTOM, pady=10)
        self.home_btn.tkraise()

        # Home Button
        user_icon_img = ctk.CTkImage(Image.open(os.getenv("HOME_ICON")), size=(int(os.getenv("DEFAULT_ICON_SIZE")), int(os.getenv("DEFAULT_ICON_SIZE"))))
        ctk.CTkButton(self.home_btn,
            text="Home",
            image=user_icon_img,
            text_color=os.getenv("WHITE_COLOR"),
            fg_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            hover_color=os.getenv("HOME_SCREEN_BG_COLOR"),
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 12)),
            command=lambda: self.accountlogic.load_home_frame(self.parent, self.frame, self.userObj)
        ).pack(padx=10)

        self.left_sidebar.pack_propagate(False)
        self.left_sidebar.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH)
        self.left_sidebar.tkraise()


    def build_main_content(self):
        """
            build_main_content() method builds the main content of the Account frame.
            This main content contains the user details.
        """
        # Main Content
        self.main_content = ctk.CTkFrame(self.frame,
            width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.8,
            height=int(os.getenv("DEFAULT_APP_HEIGHT")),
            fg_color="#f7fcfe",
            corner_radius=25
        )

    #     ctk.CTkLabel(self.main_content,
    #         text="My Cloud",
    #         fg_color="#f7fcfe",
    #         font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT4_SIZE"), 12))
    #     ).pack(pady=30, padx=30, side=tk.TOP, anchor=tk.W)

    #     ctk.CTkLabel(self.main_content,
    #         text="Hi "+self.userObj["name"]+", Welcome to your CloudDrive!",
    #         fg_color="#f7fcfe",
    #         font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"), 12))
    #     ).pack(pady=0, padx=30, side=tk.TOP, anchor=tk.W)

    #     # Main Content - Files (grid view)
    #     self.files = ctk.CTkScrollableFrame(master=self.main_content,
    #         width=int(os.getenv("DEFAULT_APP_WIDTH"))*0.8,
    #         height=int(os.getenv("DEFAULT_APP_HEIGHT"))*0.7,
    #         fg_color="#ffffff",
    #         corner_radius=25
    #     )
    #     # populate files
    #     self.homeLogic.populate_files(self.files)

    #     # configure the grid
    #     self.files.pack(side=tk.TOP, pady=10, padx=10)
    #     self.files.pack_propagate(False)

        # configure the main content
        self.main_content.pack(side=tk.RIGHT, pady=10, padx=10)
        self.main_content.tkraise()


    def remove_frame(self, frame):
        """
            remove_frame() method removes the current frame
        """
        for widget in frame.winfo_children():
            widget.destroy()
