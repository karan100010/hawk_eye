# create a function that reads a google sheet 
#reads the first row as the key
# and puts other rows as values
# return the list of all the key value pairs
 import gspread
 from oauth2client.service_account import ServiceAccountCredentials

def return_sheet_vals(sheet_name):
   
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    sheet_vals = sheet.get_all_records()
    return sheet_vals
