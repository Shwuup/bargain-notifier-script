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
        secrets = self.read_secrets()
        twilioCli = Client(secrets[0], secrets[1])
        twilioCli.messages.create(body=self.message, from_=secrets[2], to=secrets[3])


class EmailNotifier(Notifier):
    def read_secrets(self):
        pass

    def send_message(self):
        pass

