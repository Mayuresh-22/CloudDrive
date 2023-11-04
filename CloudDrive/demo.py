# This is the demo python script to run the FileStack API
from filestack import Client, Security
import time
import requests

# Initialize the client
client = Client("Af07oLPtdSVqPdz7UTtygz")

# Get the current time in seconds since the Unix epoch
now = int(time.time())

# Add one hour in seconds to the current time
expiration_time = now + 3600

print("Time: ", expiration_time, "\n")

policy = {
    "expiry": expiration_time, 
    "call": ["pick","read","stat","write","store","convert","remove","exif","writeUrl","runWorkflow"]
}
security = Security(policy, "7PDJLJSTP5G33M7FKQQE3Q4W3E")


fileinfo = client.upload(filepath="assets/img.jpg", security=security)
# fileinfo = client.upload(filepath="assets/1.pdf")
# print(fileinfo.upload_response)
print(f"URL: https://cdn.filestackcontent.com/{security.as_url_string()}/{fileinfo.upload_response['handle']} \n")
# print(f"URL: https://cdn.filestackcontent.com/{fileinfo.upload_response['handle']} \n")

# print file info
print("\nFile info:\n")
print(fileinfo.upload_response)

# download the file
print("\nDownloading the file...\n")
REQUEST=f'https://cdn.filestackcontent.com/{fileinfo.upload_response["handle"]}'
print(REQUEST, "\n")

r = requests.get(REQUEST)
if r.status_code == 200:
    open('assets/downloaded.pdf', 'wb').write(r.content)
    print("File downloaded successfully")
else:
    print("Error downloading file")

# Delete the file
# print("\nDeleting the file...\n")
# REQUEST=f'https://www.filestackapi.com/api/file/{fileinfo.upload_response["handle"]}?key=Aulnj8a0wRLERECktpnFlz&signature={security.signature}&policy={security.policy_b64}'
# print(REQUEST, "\n")

# r = requests.delete(REQUEST)
# if r.status_code == 200:
#     print("File deleted successfully")
# else:
#     print("Error deleting file")