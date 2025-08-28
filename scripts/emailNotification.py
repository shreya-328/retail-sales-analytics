import smtplib
from email.mime.text import MIMEText
import logging


from config import smtpServer, smtpPort, smtpUser, smtpPassword

def send_email(subject, body, to_email):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtpUser
        msg['To'] = ', '.join(to_email)

        with smtplib.SMTP(smtpServer, smtpPort) as server:
            server.ehlo()
            server.starttls()
            server.login(smtpUser,smtpPassword)
            server.sendmail(smtpUser, to_email, msg.as_string())
        logging.info("Email sent successfully")
        return True

    except smtplib.SMTPException as e:
        logging.error(f"SMTP error in send_email: {e}")
        return False 
       
    except Exception as e:
        logging.error(f"Error in send_email: {e}")
        return False

    # with smtplib.SMTP(smtpServer, smtpPort) as server:
    #     server.ehlo()
    #     server.starttls()
    #     server.login(smtpUser, smtpPassword)
    #     server.sendmail(smtpUser, to_email, msg.as_string())

if __name__ == '__main__':
    subject = 'Data Validation Status'
    body = 'Your data validation script ran successfully and all checks passed.'
    send_email(subject, body, ['shreyatestda@gmail.com'])
