from twilio.rest import Client
import requests
import argparse 
from bs4 import BeautifulSoup
import re
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', nargs='*')
    args = parser.parse_args()

    with open(str(Path.home()) + "/secrets.txt") as file:
        secrets = file.read().strip().split("\n")
    twilioCli = Client(secrets[0], secrets[1])
    c = requests.get("https://www.ozbargain.com.au/").content
    soup = BeautifulSoup(c)

    res = soup.find_all("h2", class_="title")
    for offers in res:
        for search_term in args.i:
            if search_term.lower() in offers['data-title'].lower():
                link = "https://www.ozbargain.com.au/node/" + offers['id'].strip("title")
                messageBody=("Bargain for %s: %s" % (search_term,link))
                twilioCli.messages.create(body=messageBody,
                                    from_=secrets[2], 
                                    to=secrets[3])

if __name__=='__main__':
    main()
