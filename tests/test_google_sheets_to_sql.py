import unittest
from unittest.mock import patch, MagicMock
import google_sheets_to_sql as gsts


class TestGoogleSheetsToSql(unittest.TestCase):

    @patch('google_sheets_to_sql.build')
    @patch('google_sheets_to_sql.Credentials.from_service_account_file')
    def test_google_sheets_service(self, mock_creds, mock_build):
        mock_creds.return_value = 'creds'
        mock_build.return_value = 'service'
        service = gsts.google_sheets_service()
        self.assertEqual(service, 'service')

    @patch('google_sheets_to_sql.google_sheets_service')
    @patch('google_sheets_to_sql.build')
    @patch('google_sheets_to_sql.Credentials.from_service_account_file')
    def test_read_sheet(self, mock_creds, mock_build, mock_service_func):
        mock_service = MagicMock()
        mock_spreadsheet = mock_service.spreadsheets.return_value
        mock_spreadsheet.values.return_value.get.return_value.execute.return_value = {
            'values': [['header1', 'header2'], ['row1col1', 'row1col2']]
        }
        mock_build.return_value = mock_service
        mock_creds.return_value = 'creds'
        mock_service_func.return_value = mock_service

        service = gsts.google_sheets_service()
        data = gsts.read_sheet(service)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], ['header1', 'header2'])

    def test_clean_row(self):
        row = ['2023-01-01', '2023-01', 'cust1', 'Male', '30', 'Electronics', '10', '100', '1000', '1500', '5', '3']
        cleaned = gsts.clean_row(row)
        self.assertEqual(cleaned[7], 100.0)
        self.assertEqual(cleaned[8], 1000.0)

    @patch('google_sheets_to_sql.pyodbc.connect')
    def test_insert_to_sql(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        data = [
            ['Date', 'Month', 'CustomerID', 'Gender', 'Age', 'ProductCategory', 'Quantity',
             'PricePerUnit', 'TotalSales', 'TotalAmount', 'TotalTransactions', 'CountUniqueProductCategory'],
            ['2025-01-01', '2025-01', 'C001', 'Male', '30', 'CatA', '5', '100', '500', '500', '1', '1']
        ]
        gsts.insert_to_sql(mock_conn, data)
        mock_cursor.executemany.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_not_called()  # Connection close is handled outside insert_to_sql

if __name__ == '__main__':
    unittest.main()

# import unittest
# from unittest.mock import patch, MagicMock
# import google_sheets_to_sql as gss

# class TestGoogleSheetsToSQL(unittest.TestCase):

#     @patch('google_sheets_to_sql.build')
#     @patch('google_sheets_to_sql.Credentials.from_service_account_file')
#     def test_google_sheets_service(self, mock_creds, mock_build):
#         mock_creds.return_value = 'creds'
#         mock_build.return_value = 'service'
#         service = gss.google_sheets_service()
#         self.assertEqual(service, 'service')

# @patch('google_sheets_to_sql.google_sheets_service')
#     @patch('google_sheets_to_sql.build')
#     @patch('google_sheets_to_sql.Credentials.from_service_account_file')
#     def test_read_sheet(self, mock_creds, mock_build, mock_service_func):
#         mock_service = MagicMock()
#         mock_spreadsheet = mock_service.spreadsheets.return_value
#         mock_spreadsheet.values.return_value.get.return_value.execute.return_value = {
#             'values': [['header1', 'header2'], ['row1col1', 'row1col2']]
#         }
#         mock_build.return_value = mock_service
#         mock_creds.return_value = 'creds'
#         mock_service_func.return_value = mock_service

#         service = gsts.google_sheets_service()
#         data = gsts.read_sheet(service)
#         self.assertEqual(len(data), 2)
#         self.assertEqual(data[0], ['header1', 'header2'])

#     def test_clean_row(self):
#         row = ['2023-01-01', '2023-01', 'cust1', 'M', '30', 'Electronics', '10', '100', '1000', '1500', '5', '3']
#         cleaned = gsts.clean_row(row)
#         self.assertEqual(cleaned[7], 100.0)
#         self.assertEqual(cleaned[8], 1000.0)


#     @patch('google_sheets_to_sql.pyodbc.connect')
#     def test_insert_to_sql(self, mock_connect):
#         mock_conn = MagicMock()
#         mock_cursor = MagicMock()
#         mock_conn.cursor.return_value = mock_cursor
#         mock_connect.return_value = mock_conn

#         sample_data = [['Date', 'Month', 'CustomerID', 'Gender', 'Age', 'ProductCategory', 'Quantity',
#                         'PricePerUnit', 'TotalSales', 'TotalAmount', 'TotalTransactions', 'CountUniqueProductCategory']]
#         sample_data.append(['2025-01-01', '2025-01', 'C001', 'M', '30', 'CatA', '5', '100', '500', '500', '1', '1'])

#         gss.insert_to_sql(sample_data)
#         mock_cursor.executemany.assert_called()
#         mock_conn.commit.assert_called()
#         mock_cursor.close.assert_called()
#         mock_conn.close.assert_called()

# if __name__ == '__main__':
#     unittest.main()
