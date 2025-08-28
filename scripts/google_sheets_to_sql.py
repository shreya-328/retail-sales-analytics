from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pyodbc

#Setting up google sheet
SCOPES=['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/shreya/Retail_Sales/sylvan-cirrus-470106-c1-23e937ea1b9a.json'

#Google sheet id and range
SPREADSHEET_ID = '1JgeXWlXHDgbPvR2DiaclK0MpDzAe_CBAkJdy2UjlT4I'
RANGE_NAME='retail_sales_dataset'


# Local SQL Server connection details
SQL_SERVER = '127.0.0.1,1433'  # localhost and port
DATABASE = 'RetailSales'
USERNAME = 'sa'  # or your SQL Server username
PASSWORD = 'Sibbu*2712'  # your password

def google_sheets_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def read_sheet(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print("No data found in Google Sheets.")
    return values

def clean_row(row):
    cleaned = []
    for i, val in enumerate(row):
        # Columns expected to be numeric (adjust indexes if needed)
        if i in [7, 8, 9, 10, 11, 12]:
            try:
                cleaned.append(float(val) if val != '' else None)
            except ValueError:
                cleaned.append(None)
        else:
            cleaned.append(val)
    return tuple(cleaned)
    # else:
    #     print("Fetched data from Google Sheets:")
    #     for row in values:
    #         print(row)
    #     return values

def insert_to_sql(conn, data):
    cursor = conn.cursor()
    insert_sql = """
       INSERT INTO SalesData 
        (Date, Month, CustomerID, Gender, Age, ProductCategory, Quantity, PricePerUnit,
         TotalSales, TotalAmount, TotalTransactions, CountUniqueProductCategory)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    rows_to_insert = [clean_row(row[1:]) for row in data[1:] if len(row) > 12]
    cursor.executemany(insert_sql, rows_to_insert)
    conn.commit()
    cursor.close()

def get_sql_connection():
    conn_str = (f'Driver={{ODBC Driver 18 for SQL Server}};'
                f'Server={SQL_SERVER};Database={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;')
    return pyodbc.connect(conn_str)

def main():
    service = google_sheets_service()
    data = read_sheet(service)
    if data:
        conn = get_sql_connection()
        insert_to_sql(conn, data)
        conn.close()
if __name__ == '__main__':
    main()
