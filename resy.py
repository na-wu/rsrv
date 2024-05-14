import requests
import urllib
import json
import logging
from typing import List, Dict, Any

# use this as the base url
BASE_URL = "https://api.resy.com"
HEADERS = {
    "origin": "https://resy.com",
    "accept-encoding": "gzip, deflate, br",
    "x-origin": "https://widgets.resy.com",
    "authorization": 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    "pragma": "no-cache",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "application/json, text/plain, */*",
    "cache-control": "no-cache",
    "authority": "api.resy.com",
    "referer": "https://resy.com",
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResyClient:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        pass

    def get(self, url, headers):
        response = requests.get(url, headers=headers)
        return response

    def post(self, url, headers, data):
        response = requests.post(url, headers=headers, data=data)
        return response

    def handle_errors(self, response):
        if response.status_code == 200:
            return

        # handle errors in the response
        if response.status_code == 404:
            logging.error("404 Not Found")
        elif response.status_code == 500:
            logging.error("500 Internal Server Error")
        elif response.status_code == 403:
            logging.error("403 Forbidden")
        elif response.status_code == 401:
            logging.error("401 Unauthorized")
        elif response.status_code == 400:
            logging.error("400 Bad Request")
        else:
            logging.error("Unknown Error")

    def handle_redirects(self, response):
        if response.is_redirect:
            logging.info("Redirecting to:", response.headers["Location"])

    def make_request(self, method, url, headers, data=None):
        if method == "GET":
            response = self.get(url, headers)
        elif method == "POST":
            response = self.post(url, headers, data)

        self.handle_errors(response)
        self.handle_redirects(response)

        return response

    def get_resy_venue_id(self, url_slug: str):
        """
        url_slug: str

        e.g. https://resy.com/cities/new-york-ny/venues/double-chicken-please?date=2024-04-13&seats=2

        in this case it would be "double-chicken-please"
        """
        # util to grab venue_id
        venue_url = "https://api.resy.com/3/venue?"
        venue_data = [("url_slug", url_slug), ("location", "ny")]

        venue_data_string = urllib.parse.urlencode(venue_data)
        venue_data_string = venue_data_string.replace("%25", "%")
        venue_url = venue_url + venue_data_string

        resp = self.make_request("GET", venue_url, HEADERS).json()
        id = resp["id"]["resy"]

        logging.info(f"Venue ID for {url_slug}: {id}")
        return id
    
    def get_slots(self, venue_id, day, party_size):
        """
        venue_id: str
        day: str
        party_size: int
        
        e.g. day = "2024-04-25"
        party_size = 2
        """
        slot_url = "https://api.resy.com/4/find?"
        slot_data = [
            ("day", day),
            ("lat", 0),
            ("long", 0),
            ("party_size", party_size),
            ("venue_id", venue_id),
        ]

        slot_data_string = urllib.parse.urlencode(slot_data)
        slot_data_string = slot_data_string.replace("%25", "%")
        slot_url += slot_data_string
        response = requests.get(slot_url, headers=HEADERS)
        data = response.json()
        parsed_data = data.get("results").get("venues")[0]
        slots = parsed_data.get("slots")

        return [slot.get("config").get("token") for slot in slots]

    def get_details(self, config_id, day, party_size):
        details_url = f"https://api.resy.com/3/details?"
        details_data = [
            ("config_id", config_id),
            ("day", day),
            ("party_size", party_size),
        ]
        config_data_string = urllib.parse.urlencode(details_data)
        config_data_string = config_data_string.replace("%25", "%")
        details_url += config_data_string
        response = requests.get(details_url, headers=HEADERS)
        response = response.json()

        return response.get("book_token").get("value")

    def book(self, book_token):
        ### Book The thing
        book_url = "https://api.resy.com/3/book"

        book_data = {
            "auth_token": self.auth_token,
            "book_token": book_token,
            "source_id": "resy.com-venue-details",
            "struct_payment_method": json.dumps({"id": 14718122}),  # CHANGE THIS
        }

        response = self.make_request("POST", book_url, HEADERS, book_data)
        if not response.status_code == 201:
            logging.error("failed to book")
            logging.info(response.json())
        else:
            logging.info("success!")
            logging.info(response.json())
