
import unittest
from unittest.mock import patch, MagicMock
import DataValidationAndMonitoring as dvm

class TestDataValidation(unittest.TestCase):

    @patch('DataValidationAndMonitoring.pyodbc.connect')
    def test_run_validation_success(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [100]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        success, msg = dvm.runValidation()
        self.assertTrue(success)
        self.assertIn("total rows", msg)

    @patch('DataValidationAndMonitoring.pyodbc.connect')
    def test_run_validation_db_error(self, mock_connect):
        mock_connect.side_effect = Exception("DB error")
        success, msg = dvm.runValidation()
        self.assertFalse(success)
        self.assertIn("An error occurred", msg)
    
    
    @patch('data_validation.build')

    @patch('data_validation.Credentials.from_service_account_file')
    def test_google_sheets_service(self, mock_creds, mock_build):
        mock_build = MagicMock()
        mock_build.return_value = 'service'
        mock_creds.return_value = 'creds'
        self.assertEqual(dvm.google_sheets_service(), 'service')

if __name__ == '__main__':
    unittest.main()
