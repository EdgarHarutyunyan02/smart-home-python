import smtplib
import ssl
import os
from dotenv import load_dotenv
import socket
from time import sleep
from email.mime.text import MIMEText

load_dotenv()


class MailService():
    def __init__(self):
        super().__init__()
        self._server = None
        self._email = os.environ.get("NOTIFICATION_EMAIL", None)
        self._password = os.environ.get("NOTIFICATION_EMAIL_PASSWORD", None)
        self._port = int(os.environ.get("EMAIL_PORT", 0))
        print(self._email)
        if self._email is None:
            print("Email not provided")
        if self._password is None:
            print("Password not provided")

    def send_message(self, message, subject, receiver=None):
        sender = self._email

        if(receiver is None):
            receiver = os.environ.get('RECEIVER_EMAIL', None)

        msg = MIMEText(message)

        msg['Subject'] = subject
        msg['From'] = 'Smart Home'
        msg['To'] = subject

        try:
            if (self._port == 465):
                # SSL connection
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", self._port, context=context) as self._server:
                    self._server.login(self._email, self._password)
                    self._server.sendmail(
                        self._email, receiver, msg.as_string())
                    print("Successfully sent the email.")
        except (smtplib.SMTPAuthenticationError, socket.gaierror, smtplib.SMTPException) as err:
            print(err)
