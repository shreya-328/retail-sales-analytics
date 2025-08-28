
import smtplib
import unittest
from unittest.mock import patch, MagicMock
from emailNotification import send_email

class TestEmailNotification(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        result = send_email(" Test Subject", "Body", ["shreyatestda@gmail.com"])
        self.assertTrue(result)

        mock_smtp.assert_called_once_with('smtp.gmail.com','587')
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()

    @patch('emailNotification.smtplib.SMTP')
    def test_send_email_smtp_exception(self,mock_smtp):
        mock_smtp.side_effect = smtplib.SMTPException("SMTP error")
        result = send_email("Subject", "Body", ["shreyatestda@gmail.com"])
        self.assertFalse(result)

    @patch('emailNotification.smtplib.SMTP')
    def test_send_email_general_exception(self,mock_smtp):
        instance= mock_smtp.return_value.__enter__.return_value
        instance.sendmail.side_effect = Exception("General error")
        result = send_email("Subject", "Body", ["shreyatestda@gmail.com"])
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
