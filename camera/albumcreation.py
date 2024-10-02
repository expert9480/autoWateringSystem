import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

# Load credentials
def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('/home/admin/Downloads/fun/camera/token.json'):
        creds = Credentials.from_authorized_user_file('/home/admin/Downloads/fun/camera/token.json', SCOPES)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/admin/Downloads/fun/camera/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/admin/Downloads/fun/camera/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Create a new album and get its ID
def create_album(album_title):
    # Authenticate
    creds = authenticate()
    
    # Build the Google Photos API service
    service = build('photoslibrary', 'v1', credentials=creds)

    # Create the album
    album_body = {
        "album": {
            "title": album_title
        }
    }
    
    # Send the request to create the album
    response = service.albums().create(body=album_body).execute()
    
    # Output the album ID
    album_id = response['id']
    print(f"Album created with ID: {album_id}")
    return album_id

if __name__ == "__main__":
    # Replace 'My New Album' with your desired album name
    album_title = "MishaJules Plant Photos"
    album_id = create_album(album_title)