usage:


```
from resy import ResyClient

def go():

	# Use ur own lol
    # Create a ResyClient object
    resy = ResyClient(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3MTYzOTIzNzQsInVpZCI6MjkzNDYwOTYsImd0IjoiY29uc3VtZXIiLCJncyI6W10sImxhbmciOiJlbi11cyIsImV4dHJhIjp7Imd1ZXN0X2lkIjoxMDU3NTEwNTF9fQ.AFV1rDzyg6Dk6LyqMrpauv-FhhDq4RlXlRdCZHEeuPSwAoBX3ffJHlbE8mPjj4U6LuKZpaJnxKju6CLHLKcndBqOAboLXbYJBuqz5iYL4ZgD9LGot3hsKtwBrCzlnbz5HpMVRMciZ8xAkk1a9c-FjGGGtRC5J1QHG4wqjtk5KLTHCLW7"
    )

    # Get the venue ID for the given URL slug
    venue_id = resy.get_resy_venue_id("jua")

    # Get the available time slots for the venue
    time_slots = resy.get_slots(venue_id, "2024-04-25", 2)

    # Get the available config IDs for the time slots
    book_token = resy.get_details(time_slots[0], "2024-04-25", 2)

    # Book a reservation using the first config ID
    resy.book(book_token)

if __name__ == "__main__":
    go()

```