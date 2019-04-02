from abc import ABC, abstractmethod
from twilio.rest import Client
import os
import smtplib


class Notifier(ABC):
    def __init__(self, message):
        self.message = message
        super().__init__()

    @abstractmethod
    def read_secrets(self, filename):
        pass

    def send_message(self):
        pass


class TextNotifier(Notifier):
    def read_secrets(self):
        with open(os.getcwd() + "/text_secrets.txt") as file:
            secrets = file.read().strip().split("\n")
            return secrets

    def send_message(self):
        account_sid, auth_token, twilio_phone_number, your_phone_number = (
            self.read_secrets()
        )
        twilioCli = Client(account_sid, auth_token)
        twilioCli.messages.create(
            body=self.message, from_=twilio_phone_number, to=your_phone_number
        )


class EmailNotifier(Notifier):
    def read_secrets(self):
        with open(os.getcwd() + "/email_secrets.txt") as file:
            secrets = file.read().strip().split("\n")
        return secrets

    def send_message(self):
        email, password = self.read_secrets()
        smtpObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtpObj.login(email, password)
        smtpObj.sendmail(
            email, email, "Subject: OzBargain Notification!\n" + self.message
        )
        smtpObj.quit()

