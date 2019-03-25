import requests
import argparse
from bs4 import BeautifulSoup
from pathlib import Path
import shelve
import logging
from notifiers import TextNotifier, EmailNotifier


def get_html_doc():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"
    }
    html_content = requests.get(
        "https://www.ozbargain.com.au/", headers=headers
    ).content
    return BeautifulSoup(html_content, "html.parser")


def setup_logging():
    logging.basicConfig(
        filename=str(Path.home()) + "/bargain_error.log",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_elegible_bargains(search_terms):
    seen_bargains = shelve.open("seen_deals")
    soup = get_html_doc()
    res = soup.find_all(class_="node-ozbdeal")
    offers_message = ""
    for offers in res:
        offer_info = offers.find("h2", class_="title")
        for search_term in search_terms:
            link = "https://www.ozbargain.com.au/node/" + offer_info["id"].strip(
                "title"
            )
            if (
                search_term.lower() in offer_info["data-title"].lower()
                and link not in seen_bargains
            ):
                print(offer_info["data-title"])
                offers_message += "%s\n%s\n\n" % (offer_info["data-title"], link)
                seen_bargains[link] = offer_info["data-title"]
    seen_bargains.close()
    return offers_message


def main():
    try:
        setup_logging()
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", nargs="*")
        parser.add_argument("-n")
        args = parser.parse_args()
        message = get_elegible_bargains(args.i)

        if message:
            if args.n == "email":
                notifier = EmailNotifier(message)
            elif args.n == "text":
                notifier = TextNotifier(message)
            notifier.send_message()
            print("Message sent successfully!")
            logging.debug("message sent: %s", message)
    except Exception as e:
        print(e)
        logging.exception("Exception occured")


if __name__ == "__main__":
    main()
