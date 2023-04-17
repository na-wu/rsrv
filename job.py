# RESY.PY
import requests
import urllib
import json
import datetime
import time
import pprint
from datetime import timedelta
import settings

'''
1. get venue id DONE
2. hit slot query -> save config.id DONE
3. Send Config ID DONE
4. Save book_token.value DONE
5. send book request
'''


headers = {
	'origin': 'https://resy.com',
	'accept-encoding': 'gzip, deflate, br', 
	'x-origin': 'https://widgets.resy.com', 
	'accept-language': 'en-US,en;q=0.9',
	'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"', 
	'pragma': 'no-cache', 
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
	'content-type': 'application/x-www-form-urlencoded', 
	'accept': 'application/json, text/plain, */*', 
	'cache-control': 'no-cache', 
	'authority': 'api.resy.com', 
	'referer': 'https://resy.com'
	}

userAuthToken = settings.user_auth_token


def get_resy_venue_id(url_slug):
	# util to grab venue_id
	# from job import get_resy_venue_id
	# venue_id = get_resy_venue_id("restaurant-slug")
	# e.g. get_resy_venue_id("cote")
		venue_url = "https://api.resy.com/3/venue?"
		venue_data = [
			('url_slug', url_slug),
			('location', 'ny')
		]

		venue_data_string = urllib.parse.urlencode(venue_data)
		venue_data_string = venue_data_string.replace("%25", "%") #fix encoding percent bug 
		venue_url = venue_url + venue_data_string # Concat Stirng Builder

		resp = requests.get(venue_url, headers=headers).json()
		id = resp['id']['resy']

		print(f"Venue ID for {url_slug}: {id}")
		return id

def book(book_token):
	### Book The thing
	book_url = "https://api.resy.com/3/book"

	book_data = {
		'auth_token': userAuthToken,
		'book_token': book_token, 
		'source_id': 'resy.com-venue-details',
		'struct_payment_method': json.dumps({"id":14718122}) # CHANGE THIS
		}

	response = requests.post(book_url, headers=headers, data=book_data)
	if not response.status_code == 201:
		print("failed to book")
		pprint.pprint(response.json())		
	else:
		print("success!")
		pprint.pprint(response.json())

def job(target_date, party_size, venue_id, time_floor, time_ceiling):
	print("Start ResyBot")
	time_floor = time_floor or None # today_plus_one_week.replace(hour=7, minute=30, second=0, microsecond=0)
	time_ceiling = time_ceiling or None # today_plus_one_week.replace(hour=7, minute=30, second=0, microsecond=0)

	day = target_date.date()

	slot_url = 'https://api.resy.com/4/find?'
	slot_data = [
		('day', day),
		('lat', 0),
		('long', 0),
		('party_size', party_size),
		('venue_id', venue_id)
		]

	slot_data_string = urllib.parse.urlencode(slot_data)
	slot_data_string = slot_data_string.replace("%25", "%") #fix encoding percent bug 
	slot_url += slot_data_string # Concat Stirng Builder

	### Send Slot Query Request & Save Config ID ###
	response = requests.get(slot_url, headers=headers)
	json_data = response.json()

	print(json_data["results"]["venues"])

	### Collection of config ideas
	config_ids = []

	for i in json_data["results"]["venues"][0]["slots"]:
		token = i["config"]["token"]
		res_data_time = i["date"]["start"] 

		datetime_object = datetime.datetime.strptime(res_data_time, '%Y-%m-%d %H:%M:%S')

		if time_floor and not time_ceiling:
			config_ids.append(token) if datetime_object >= time_floor else None
			continue

		if time_ceiling and not time_floor:
			config_ids.append(token) if datetime_object <= time_ceiling else None
			continue

		if time_floor and time_ceiling:
			config_ids.append(token) if datetime_object <= time_ceiling and datetime_object >= time_floor else None
			continue

		config_ids.append(token)

	if not config_ids:
		print("None with time slots specified")
		print("defaulting to earliest available")

	bookables = config_ids or [i["config"]["token"] for i in json_data["results"]["venues"][0]["slots"]]

	if bookables:
		
		### Now we have config ids we need to send 
		config_url = 'https://api.resy.com/3/details?'
		config_data = [
			('config_id', config_ids[0]),
			('day', day),
			('party_size', party_size)
			]

		config_data_string = urllib.parse.urlencode(config_data)
		config_data_string = config_data_string.replace("%25", "%") #fix encoding percent bug 
		config_url += config_data_string # Concat Stirng Builder

		response = requests.get(config_url, headers=headers)
		json_data = response.json()


		if "book_token" not in json_data:
			print("No book token available") 
		else:
			book_token = json_data["book_token"]["value"]
			book(book_token)
			
	else:
		print(f"no config ids for {day}") 

