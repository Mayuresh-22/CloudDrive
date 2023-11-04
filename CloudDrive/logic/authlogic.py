"""
    AuthLogic class is used to implement user authentication logic
"""

# import modules
import os
from view.homeframe import HomeFrame
from dotenv import load_dotenv
import requests

from view.homeframe import HomeFrame
load_dotenv(".env")

class AuthLogic():
    """
        This class handels the logic behind the auth frame
        (Login/Register), selecting cloud provider, validating API etc
    """
    def auth_user_login(parent, current, **kwargs):
        """
            This method authenticates the user by hitting the login API.
            - username: the username of the user
            - password: the password of the user
        """
        # Hit the login API if fields are not empty
        if kwargs["username"] != "" and kwargs["password"] != "":
            url = os.getenv("APP_BASE_URL")+os.getenv("USERS_ENDPOINT")+os.getenv("LOGIN_ENDPOINT")
            try:
                resp =  requests.post(url,
                            headers={"Content-Type": "application/json"},
                            json={"username": kwargs["username"], "password": kwargs["password"]}
                        )
                if resp.status_code == 200 and resp.json()["status"] == "success":
                    # Redirect to Home frame
                    HomeFrame(parent, current, resp.json())
                else:
                    kwargs["errorlabel"].configure(text=resp.json()["message"])
            except:
                kwargs["errorlabel"].configure(text="Server error occurred. Try again after sometime.")


    def auth_user_register(parent, current, **kwargs):
        """
            This method registers the user by hitting the register API.
            - name: the name of the user
            - username: the username of the user
            - password: the password of the user
            - cloud_provider: the cloud provider of the user
            - api_key: the api key of the user
        """
        # Hit the register API if fields are not empty
        if kwargs.get("name") != "" and kwargs.get("username") != "" and kwargs.get("password") != "" and kwargs.get("cloud_provider") != "" and kwargs.get("api_key") != "":
            url = os.getenv("APP_BASE_URL")+os.getenv("USERS_ENDPOINT")+os.getenv("REGISTER_ENDPOINT")
            try:
                resp = requests.post(url,
                            headers={"Content-Type": "application/json"},
                            json={"name": kwargs["name"], "username": kwargs["username"], "password": kwargs["password"], "cloud_provider": kwargs["cloud_provider"], "cloud_provider_api_key": kwargs["api_key"]}
                        )
                if resp.status_code == 200 and resp.json()["status"] == "success":
                    # Redirect to Home frame
                    HomeFrame(parent, current, resp.json())
                else:
                    kwargs["errorlabel"].configure(text=resp.json()["message"])
            except:
                kwargs["errorlabel"].configure(text="Server error occurred. Try again after sometime.")
