from twilio.rest import Client
import requests
import argparse 
from bs4 import BeautifulSoup
from pathlib import Path
import shelve
import sys
import logging

def read_secrets(filename):
    with open(str(Path.home()) + '/'+filename) as file:
        secrets = file.read().strip().split('\n')
        return secrets

def get_html_doc():
    headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    html_content = requests.get('https://www.ozbargain.com.au/', headers=headers).content
    return BeautifulSoup(html_content, 'html.parser')

def setup_logging():
    logging.basicConfig(
    filename=str(Path.home()) + '/bargain_error.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def send_text_message(message_body):
    secrets = read_secrets('secrets.txt')
    twilioCli = Client(secrets[0], secrets[1])
    twilioCli.messages.create(body=message_body,
                        from_=secrets[2], 
                        to=secrets[3])
    print(message_body)

def get_elegible_bargains(search_terms):
        seen_bargains = shelve.open('seen_deals')
        soup = get_html_doc()
        res = soup.find_all(class_='node-ozbdeal')
        offers_message = ''
        for offers in res:
            offer_info = offers.find('h2', class_='title')
            for search_term in search_terms:
                link = 'https://www.ozbargain.com.au/node/' + offer_info['id'].strip('title')
                if search_term.lower() in offer_info['data-title'].lower() and link not in seen_bargains:
                    offers_message += ('%s\n%s\n\n' % (offer_info['data-title'],link))
                    seen_bargains[link] = offer_info['data-title']
        seen_bargains.close()
        return offers_message

def main():
    try:
        setup_logging()
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', nargs='*')
        args = parser.parse_args()
        message = get_elegible_bargains(args.i)
        if message:
            send_text_message(message)
            logging.debug('message sent: %s', message)
    except:
        logging.exception('Exception occured')
    
if __name__=='__main__':
    main()
