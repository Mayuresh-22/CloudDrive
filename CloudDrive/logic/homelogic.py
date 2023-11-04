"""
    HomeLogic is rhe class that handles the logic for the home page.
    This class __init__ method takes the user object as the parameter.
    This class has the following methods:
    - launch_file_explorer(): This method launches the file explorer of the system.
    - upload_file(): This method is the global method to upload the file to the cloud.

    This class has the following attributes:
    - userObj: the user object, which contains the user details (JSON)
    - cloudSetObj: the cloud provider setup object (CloudSetup)
    - filehandler: the file handler object for the cloud provider,
                   which handles the file actions (Any cloud provider type)

"""

# Import the required modules
from tkinter import filedialog
from logic.cloud import CloudSetup, Filestack


class HomeLogic:
    """
        HomeLogic is the class that handles the logic for the home page.
        This class __init__ method takes the user object as the parameter.
        This class has the following methods:
        - launch_file_explorer(): This method launches the file explorer of the system.
        - upload_file(): This method is the global method to upload the file to the cloud.

        This class has the following attributes:
        - userObj: the user object, which contains the user details (JSON)
        - cloudSetObj: the cloud provider setup object (CloudSetup)
        - filehandler: the file handler object for the cloud provider,
                    which handles the file actions (Any cloud provider type)

    """
    def __init__(self, userObj):
        """
            This is the constructor of the HomeLogic class.
            - userObj: the user object, which contains the user details
        """
        self.userObj = userObj
        self.cloudSetObj = CloudSetup(userObj["cloud_provider"], userObj["cloud_provider_api_key"])
        # Create File handler object for the cloud provider
        if userObj["cloud_provider"] == "filestack":
            self.filehandler = Filestack()


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
        filelink = self.filehandler.upload_file(file)
        print(filelink.upload_response)
