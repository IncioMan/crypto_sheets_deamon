from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheets:

    def __init__(self, sheet_id):
        creds = None
        creds = credentials = service_account.Credentials.from_service_account_file("credentials/gs_credentials.json", scopes=SCOPES)
        print("Connecting to Google Sheets APIs..")
        self.service = build('sheets', 'v4', credentials=creds)
        self.sheet_id = sheet_id

    def get_range(self, range):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id,
                                    range=range).execute()
        values = result.get('values', [])
        df = pd.DataFrame(values)
        return df
        

def main():
    sheet = GoogleSheets("1cr49gsJkoScgMo9o792cjoOb_gBJqJwSebX3HWFUnKA")
    df = sheet.get_range("Crypto!A2:A")

if __name__ == '__main__':
    main()