"""
    AuthLogic class is used to implement user authentication logic
"""

# import modules
import os
from dotenv import load_dotenv
import requests
load_dotenv(".env")

class AuthLogic():
    """
        This class handels the logic behind the auth frame
        (Login/Register), selecting cloud provider, validating API etc
    """
    def auth_user_login(username, password):
        """
            This method authenticates the user.
            - username: the username of the user
            - password: the password of the user
        """
        # Hit the login API if fields are not empty
        if username != "" and password != "":
            url = os.getenv("APP_BASE_URL")+os.getenv("USERS_ENDPOINT")+os.getenv("LOGIN_ENDPOINT")
            print(url)
            resp =  requests.post(url,
                        headers={"Content-Type": "application/json"},
                        json={"username": username, "password": password}
                    )
            if resp.status_code == 200:
                # Login successful
                print("Login status", resp.json())

    def auth_user_register(name, username, password, cloud_provider, api_key):
        """
            This method registers the user.
            - name: the name of the user
            - username: the username of the user
            - password: the password of the user
            - cloud_provider: the cloud provider of the user
            - api_key: the api key of the user
        """
        # Hit the register API if fields are not empty
        if name != "" and username != "" and password != "" and cloud_provider != "" and api_key != "":
            url = os.getenv("APP_BASE_URL")+os.getenv("USERS_ENDPOINT")+os.getenv("REGISTER_ENDPOINT")
            print(url)
            resp = requests.post(url,
                        headers={"Content-Type": "application/json"},
                        json={"name": name, "username": username, "password": password, "cloud_provider": cloud_provider, "cloud_provider_api_key": api_key}
                    )
            if resp.status_code == 200:
                # Registration successful
                print("Registration status", resp.json())
