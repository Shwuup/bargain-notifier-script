from twilio.rest import Client
import requests
from bs4 import BeautifulSoup

with open("secrets.txt") as file:
    secrets = file.read().strip().split("\n")

twilioCli = Client(secrets[0], secrets[1])

# message = twilioCli.messages.create(body="how you doing?", 
#                                     from_=secrets[2], 
#                                     to=secrets[3])

