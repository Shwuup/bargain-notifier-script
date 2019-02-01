from twilio.rest import Client
import requests
import argparse 
from bs4 import BeautifulSoup
from pathlib import Path
import shelve

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', nargs='*')
    args = parser.parse_args()

    already_seen = shelve.open("seen_deals")
    with open(str(Path.home()) + "/secrets.txt") as file:
        secrets = file.read().strip().split("\n")
    twilioCli = Client(secrets[0], secrets[1])
    c = requests.get("https://www.ozbargain.com.au/").content
    soup = BeautifulSoup(c)

    res = soup.find_all("h2", class_="title")
    for offers in res:
        for search_term in args.i:
            link = "https://www.ozbargain.com.au/node/" + offers['id'].strip("title")
            if search_term.lower() in offers['data-title'].lower() and link not in already_seen:
                already_seen[link] = offers['data-title']
                messageBody=("%s\n%s" % (offers['data-title'],link))
                twilioCli.messages.create(body=messageBody,
                                    from_=secrets[2], 
                                    to=secrets[3])
                print("link sent: " + link)
    already_seen.close()

if __name__=='__main__':
    main()
