"""
    AuthLogic class is used to implement user authentication logic
"""

import requests

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
        # Hit the login API
        resp =  requests.post("http://127.0.0.1:5000/users/login/",
                    headers={"Content-Type": "application/json"},
                    json={"username": username, "password": password}
                )
        if resp.status_code == 200:
            # Login successful
            print("Login status", resp.json())
        