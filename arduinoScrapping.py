import logging
import os
import serial
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime

# SCOPES to read/write to Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of your Google Sheet (replace this with your actual Sheet ID)
SPREADSHEET_ID = '14Vf1kVEO3N6wA0wmR_M-Y68WkD7t1jYBhvhdfchbvzM'
RANGE_NAME = 'Sheet1!B1'  # Adjust this to where you want to start writing data

# Function to authenticate and return the Google Sheets service
def get_sheets_service():
    creds = None
    # Check if token.json exists for existing credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no credentials or they are invalid, go through authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/home/mishajules/Downloads/credentials.json', SCOPES) #replace credentials.json with your client secret you downloaded as part of the OAuth
            creds = flow.run_local_server(port=0)
        # Save credentials to token.json for future runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Build the Sheets service
    service = build('sheets', 'v4', credentials=creds)
    return service

def append_data_to_sheet(service, data):
    try:
        body = {
            'values': [data]
        }
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
        print("Data appended to sheet:", data)
    except HttpError as error:
        print(f"An error occurred: {error}")


# Set up serial communication with the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change this to your correct serial port

# Get Google Sheets service
sheets_service = get_sheets_service()

# Continuously read from Arduino and write to Google Sheets


# while True:
#     if ser.in_waiting:
#         data = ser.readline().decode('utf-8').rstrip()
#         print(f"Read from Arduino: {data}")

#         # Get the current timestamp
#         current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         if data.startswith("~"):
#             json_data_str = data[1:].rstrip('|')
#             try:
#                 json_data = json.loads(json_data_str)
#                 temperature_value = json_data['value']  # Extract the temperature value
#                 # Prepare data to append: [time, light, temperature]
#                 append_data_to_sheet(sheets_service, [current_time, '', temperature_value])  # Light is empty for now
#                 print(f"Temperature value appended: {temperature_value}")
#             except json.JSONDecodeError:
#                 print("Error decoding JSON data")
#             except KeyError:
#                 print("Key 'value' not found in the JSON data")
#         else:
#             try:
#                 light_value = float(data)  # Convert to float if needed
#                 # Now append the light value with the current time and empty temperature
#                 append_data_to_sheet(sheets_service, [current_time, light_value, ''])  # Temperature is empty for now
#                 print(f"Light value appended: {light_value}")
#             except ValueError:
#                 print("Error converting light value to float")

light_value = None
temperature_value = None

try:
    while True:
        if ser.in_waiting:
            data = ser.readline().decode('utf-8').rstrip()
            logging.info("Read from Arduino: %s", data)

            # Get the current timestamp
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if data.startswith("~"):
                json_data_str = data[1:].rstrip('|')
                try:
                    json_data = json.loads(json_data_str)
                    temperature_value = json_data.get('value')  # Get temperature value
                except (json.JSONDecodeError, KeyError) as e:
                    logging.error("Error processing JSON data: %s", e)
            else:
                try:
                    light_value = float(data)  # Convert to float
                except ValueError:
                    logging.error("Error converting light value to float")

            # Only append when both values are available
            if light_value is not None and temperature_value is not None:
                append_data_to_sheet(sheets_service, [current_time, light_value, temperature_value])
                # Reset values after appending
                light_value = None
                temperature_value = None

except KeyboardInterrupt:
    logging.info("Program terminated by user")
finally:
    ser.close()