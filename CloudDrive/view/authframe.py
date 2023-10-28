from logic.authlogic import AuthLogic
import customtkinter as ctk
from dotenv import load_dotenv
import os

load_dotenv(".env")


class AuthFrame():
    """
        This class defines the auth frame. Auth frame is the first frame of the app. 
        User can login or register from this frame.
        - parent: the parent of the frame
    """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent, 
            fg_color="#f7fcfe",
            width=int(os.getenv("DEFAULT_APP_WIDTH")),
            height=int(os.getenv("DEFAULT_APP_HEIGHT"))
        )
        self.frame.grid(row=0, column=0)
        self.frame.pack_propagate(False)
        self.frame.tkraise()
        self.build()

    def build(self):
        """
            build() method builds the auth frame
        """
        ctk.CTkLabel(self.frame,
            text=os.getenv("APP_TITLE"),
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT2_SIZE"), 12)),
            text_color=os.getenv("PRIMARY_COLOR_MED")
        ).pack(pady=60)
        
        ctk.CTkLabel(self.frame,
            text="Login or Register",
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT4_SIZE"))),
            text_color="#1B387C"
        ).pack(pady=0)
        
        # Auth details form
        self.auth_username = ctk.CTkEntry(self.frame,
            width=300,
            height=40,
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            border_width=1,
            placeholder_text="Username",
            placeholder_text_color="#adb5bd"
        )
        self.auth_username.pack(pady=10)
        self.auth_username.insert(0, "admin")
        
        self.auth_password = ctk.CTkEntry(self.frame,
            width=300,
            height=40,
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            border_width=1,
            placeholder_text="Password",
            placeholder_text_color="#adb5bd",
        )
        self.auth_password.pack(pady=5)
        self.auth_password.insert(0, "admin")
        
        self.login_btn = ctk.CTkButton(self.frame,
            text="Login",
            width=300,
            height=40,
            fg_color=os.getenv("PRIMARY_COLOR_MED"),
            text_color="#E3F5FD",
            hover_color="#1B387C",
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            command=lambda: AuthLogic.auth_user_login(self.parent, self.frame, self.auth_username.get(), self.auth_password.get())
        )
        self.login_btn.pack(pady=5)
        
        self.register_btn = ctk.CTkButton(self.frame,
            text="I don't have an account. Register?",
            width=300,
            height=40,
            fg_color="transparent",
            text_color="#1B387C",
            hover=False,
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            command=lambda: self.build_register()
        )
        self.register_btn.pack(pady=10)



    def build_register(self):
        """This method builds the register form."""

        self.api_entry_widget_track = 0 # track variable for api entry widget

        # Hide loginbtn form
        self.login_btn.pack_forget()
        self.register_btn.pack_forget()

        # User Real name Entry widget
        self.auth_name = ctk.CTkEntry(self.frame,
            width=300,
            height=40,
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            border_width=1,
            placeholder_text="Your name",
            placeholder_text_color="#adb5bd"
        )
        self.auth_name.pack(pady=5)

        # Cloud provider name Entry widget
        self.auth_cloud_provider = ctk.CTkComboBox(self.frame,
            width=300,
            height=40,
            values=["Choose your Cloud Provider", "Filestack"],
            button_color=os.getenv("PRIMARY_COLOR_MED"),
            button_hover_color="#1B387C",
            command=self.on_cloud_provider_selected
        )
        self.auth_cloud_provider.pack(pady=5)

        # API key Entry widget
        self.auth_api_key = ctk.CTkEntry(self.frame,
            width=300,
            height=40,
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            border_width=1,
            placeholder_text=f"Your API key",
            placeholder_text_color="#adb5bd"
        )

        # Register button widget
        self.register_btn = ctk.CTkButton(self.frame,
            text="Register",
            width=300,
            height=40,
            fg_color=os.getenv("PRIMARY_COLOR_MED"),
            text_color="#E3F5FD",
            hover_color="#1B387C",
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            command=lambda: AuthLogic.auth_user_register(self.parent, self.frame, name = self.auth_name.get(), username = self.auth_username.get(), password = self.auth_password.get(), cloud_provider = self.auth_cloud_provider.get(), api_key = self.auth_api_key.get())
        )

        # back button widget
        self.back_btn = ctk.CTkButton(self.frame,
            text="Back",
            width=300,
            height=40,
            fg_color="transparent",
            text_color="#1B387C",
            hover=False,
            font=(os.getenv("DEFAULT_FONT"), int(os.getenv("HEADING_FONT6_SIZE"))),
            command=lambda: self.on_back_btn_clicked()
        )
        self.back_btn.pack(pady=10)

    def on_cloud_provider_selected(self, value):
        if value != "Choose your Cloud Provider" and self.api_entry_widget_track != 1:
            print("selected: ", value)
            self.back_btn.pack_forget()
            self.auth_api_key.pack(pady=5)
            self.register_btn.pack(pady=5)
            self.back_btn.pack(pady=10)
            self.api_entry_widget_track = 1
        else:
            self.api_entry_widget_track = 0
            self.auth_api_key.pack_forget()
            self.register_btn.pack_forget()

    def on_back_btn_clicked(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.build()

    def remove_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()