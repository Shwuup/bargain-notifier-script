from twilio.rest import Client
import requests
import argparse 
from bs4 import BeautifulSoup
from pathlib import Path
import shelve
import sys
import logging

def read_secrets(filename):
    with open(str(Path.home()) + "/"+filename) as file:
        secrets = file.read().strip().split("\n")
        return secrets

def main():
    try:
        logging.basicConfig(filename=str(Path.home()) + "/bargain_error.log",level=logging.DEBUG)
        secrets = read_secrets("secrets.txt")
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', nargs='*')
        args = parser.parse_args()

        seen_bargains = shelve.open("seen_deals")
        twilioCli = Client(secrets[0], secrets[1])
        headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}
        c = requests.get("https://www.ozbargain.com.au/", headers=headers).content
        soup = BeautifulSoup(c, 'html.parser')

        res = soup.find_all("h2", class_="title")
        for offers in res:
            for search_term in args.i:
                link = "https://www.ozbargain.com.au/node/" + offers['id'].strip("title")
                if search_term.lower() in offers['data-title'].lower() and link not in seen_bargains:
                    messageBody=("%s\n%s" % (offers['data-title'],link))
                    twilioCli.messages.create(body=messageBody,
                                        from_=secrets[2], 
                                        to=secrets[3])
                    logging.debug("link sent: %s", link)
                    seen_bargains[link] = offers['data-title']
    except:
        logging.exception("Exception occured")
    seen_bargains.close()

if __name__=='__main__':
    main()
