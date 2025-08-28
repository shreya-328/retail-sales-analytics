from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pyodbc
import logging
from config import DatabaseConnString


# Setup for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/shreya/Retail_Sales/sylvan-cirrus-470106-c1-23e937ea1b9a.json'

SPREADSHEET_ID = '1JgeXWlXHDgbPvR2DiaclK0MpDzAe_CBAkJdy2UjlT4I'
RANGE_NAME = 'retail_sales_dataset'

# # SQL Server connection details
# SQL_SERVER = '127.0.0.1,1433'
# DATABASE = 'RetailSales'
# USERNAME = 'sa'
# PASSWORD = 'Sibbu*2712'

def google_sheets_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)

def get_sheets_row_count(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return max(0, len(values) - 1)

def get_sql_server_connection():
    conn_str = (f'Driver={{ODBC Driver 18 for SQL Server}};'
                f'Server={SQL_SERVER};Database={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;')
    return pyodbc.connect(conn_str)

def get_sql_server_row_count(cursor):
    cursor.execute("SELECT COUNT(*) FROM SalesData")
    return cursor.fetchone()[0]

def check_missing_and_invalid(cursor):
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN Date IS NULL THEN 1 ELSE 0 END) AS DateMissing,
            SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS CustomerIDMissing,
            SUM(CASE WHEN Quantity <= 0 THEN 1 ELSE 0 END) AS InvalidQuantity
        FROM SalesData
    """)
    return cursor.fetchone()

def check_duplicates(cursor):
    cursor.execute("""
        SELECT Transactions, COUNT(*) AS CountDup
        FROM SalesData
        GROUP BY Transactions
        HAVING COUNT(*) > 1
    """)
    return cursor.fetchall()

def main():
    service = google_sheets_service()
    sheets_count = get_sheets_row_count(service)

    conn = get_sql_server_connection()
    cursor = conn.cursor()

    sql_count = get_sql_server_row_count(cursor)
    print(f"Google Sheets Row Count: {sheets_count}")
    print(f"SQL Server SalesData Row Count: {sql_count}")

    if sheets_count == sql_count:
        print("Row counts match! Data loaded correctly.")
    else:
        print("Row count mismatch! Check data loading process.")

    missing_date, missing_cust, invalid_qty = check_missing_and_invalid(cursor)
    print(f"Missing Date values: {missing_date}")
    print(f"Missing CustomerID values: {missing_cust}")
    print(f"Invalid Quantity (<= 0): {invalid_qty}")

    duplicates = check_duplicates(cursor)
    if duplicates:
        print("Duplicate Transactions found:")
        for trans, count in duplicates:
            print(f" Transaction {trans}, Count: {count}")
    else:
        print("No duplicate Transactions found.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()


def runValidation():
    try:
        conn=pyodbc.connect(DatabaseConnString)
        cursor=conn.cursor()

        cursor.execute("Select count(*) from SalesData")
        rowCount=cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return True, f"Validation successful, total rows: {rowCount}"

    except pyodbc.Error as e:
        logging.error(f"Database error occurred: {e}")
        return False, f"Database error occurred: {e}"

    except Exception as e:
        logging.error(f"An error occurred during validation: {e}")
        return False, f"An error occurred: {e}"
