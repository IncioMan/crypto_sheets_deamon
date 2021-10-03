from __future__ import print_function
import os.path
import gspread
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheets:

    def __init__(self, sheet_id):
        print("Connecting to Google Sheets APIs..")
        self.gc = credentials = gspread.service_account("credentials/gs_credentials.json", scopes=SCOPES)
        self.sheet_id = sheet_id
        print("Connected to Google Sheets APIs")

    def get_range(self, sheet, column):
        # Call the Sheets API
        sheet = self.gc.open_by_key(self.sheet_id).worksheet(sheet)
        values = sheet.col_values(column)
        df = pd.DataFrame(values)
        return df

    def get_ranges(self, sheet, columns):
        # Call the Sheets API
        sheet = self.gc.open_by_key(self.sheet_id).worksheet(sheet)
        values = {}
        max_length = 0
        for col in columns:
            values[col] = sheet.col_values(col)
            max_length = max(max_length, len(values[col]))
        #uniform lengths of columns
        for col in columns:
            values[col] = values[col] + ['']*(max_length-len(values[col]))
        
        df = pd.DataFrame(values)
        return df

    def write_to_range(self, sheet, values, range):
        # Call the Sheets API
        sheet = self.gc.open_by_key(self.sheet_id).worksheet(sheet)
        sheet.update(range, values)
        

def main():
    sheet = GoogleSheets("1cr49gsJkoScgMo9o792cjoOb_gBJqJwSebX3HWFUnKA")
    df = sheet.write_to_range("test", [["ciao"],["bello"]], "C6:A2")

if __name__ == '__main__':
    main()