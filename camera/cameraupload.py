import os
import time
import requests
from picamera2 import Picamera2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build

# Google Photos API scopes
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary',
    'https://www.googleapis.com/auth/photoslibrary.sharing',
    'https://www.googleapis.com/auth/photos.upload',
    'https://www.googleapis.com/auth/photoslibrary.readonly'
]

def authenticate():
    creds = None
    if os.path.exists('/home/admin/Downloads/fun/camera/token.json'):
        try:
            creds = Credentials.from_authorized_user_file('/home/admin/Downloads/fun/camera/token.json', SCOPES)
        except Exception as e:
            print(f"Failed to load credentials from token.json: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("Token refreshed successfully.")
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None
        else:
            if not os.path.exists('/home/admin/Downloads/fun/camera/credentials.json'):
                raise FileNotFoundError("The credentials.json file is missing. Please download it from Google Cloud Console.")
            try:
                flow = InstalledAppFlow.from_client_secrets_file('/home/admin/Downloads/fun/camera/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("User authenticated successfully.")
            except Exception as e:
                print(f"Failed to authenticate user: {e}")
                return None

        if creds:
            with open('/home/admin/Downloads/fun/camera/token.json', 'w') as token:
                token.write(creds.to_json())
            print("Credentials saved to token.json.")

    if creds is None:
        raise ValueError("Credentials are not initialized. Please check the authentication process.")

    return creds


def upload_photo(creds, photo_path, album_id):
    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': os.path.basename(photo_path),
        'X-Goog-Upload-Protocol': 'raw'
    }

    with open(photo_path, 'rb') as photo_file:
        response = requests.post(url, headers=headers, data=photo_file)

    if response.status_code == 200:
        upload_token = response.text
        print('Upload successful! Upload token:', upload_token)

        create_body = {
            "newMediaItems": [
                {
                    "description": "Uploaded via API",
                    "simpleMediaItem": {
                        "uploadToken": upload_token
                    }
                }
            ],
            "albumId": album_id  # Using the provided album ID
        }

        create_url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
        create_response = requests.post(create_url, headers={'Authorization': f'Bearer {creds.token}'}, json=create_body)

        if create_response.status_code == 200:
            print('Media item created successfully:', create_response.json())
        else:
            print('Failed to create media item:', create_response.json())
    else:
        print('Upload failed:', response.content)

# def take_photo():
#     with picamera.PiCamera() as camera:
#         time.sleep(2)  # Allow camera to warm up
#         timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
#         folder_path = "/home/admin/Downloads/fun/camera"
#         os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
#         filename = os.path.join(folder_path, f"photo_{timestamp}.jpg")
#         camera.capture(filename)
#         print(f"Photo saved as {filename}")
#         return filename  # Return the filename for uploading
    
def take_photo():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = "/home/admin/Downloads/fun/camera/Photos"
    filename = os.path.join(folder_path, f"photo_{timestamp}.jpg")
    picam2.capture_file(filename)
    picam2.stop()
    return filename

def main():
    creds = authenticate()
    # import requests
    # _header={'Authorization': 'Bearer {}'.format(creds.token), 'Content-Type': 'application/json'}
    # _google_albums_url = 'https://photoslibrary.googleapis.com/v1/albums'
    # _body = {"album": {'title': 'plant_progress'} }
    # _response = requests.post(_google_albums_url, headers=_header, data=str(_body))
    # print(_response.text)
    # _response = requests.get(_google_albums_url, headers=_header)
    # print(_response.text)

    # AG3xhmZvLoDb0Nw81KYEP36PVrIpXuep-f1y_EET0FG_NTK4YgoNrgnrZvZM6SYCxEmu05HK3jC5

    # with build("photoslibrary", "v1", static_discovery=False, credentials=creds) as service:
    #     #resources = service._resourceDesc["resources"]
    #     #results=service.albums().list(pageSize=10,fields="nextPageToken,albums(id,title)").execute()
    #     results=service.albums().list().execute()
    #     print(results)
    #     items = results.get('albums',[])
    #     if not items:
    #         print("no albums")
    #     else:            
    #         for item in items:
    #             print('{0} ({1})'.format(item['title'].encode('utf8'), item['id']))
        #for group in resources: 
        #    for method in resources[group]["methods"]:
        #        print(f"{resources [group]['methods'][method]['id']} with params: " 
        #              f"{resources [group]['methods'][method]['parameters']}")

    album_id = "AG3xhmZvLoDb0Nw81KYEP36PVrIpXuep-f1y_EET0FG_NTK4YgoNrgnrZvZM6SYCxEmu05HK3jC5"  # Fixed album ID
    photo_path = take_photo()  # Take a photo and get the path
    upload_photo(creds, photo_path, album_id)  # Upload the photo to the specified album

if __name__ == '__main__':
    main()