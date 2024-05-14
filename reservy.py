from resy import ResyClient


def go():
    # Create a ResyClient object
    resy = ResyClient(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3MTYzOTIzNzQsInVpZCI6MjkzNDYwOTYsImd0IjoiY29uc3VtZXIiLCJncyI6W10sImxhbmciOiJlbi11cyIsImV4dHJhIjp7Imd1ZXN0X2lkIjoxMDU3NTEwNTF9fQ.AFV1rDzyg6Dk6LyqMrpauv-FhhDq4RlXlRdCZHEeuPSwAoBX3ffJHlbE8mPjj4U6LuKZpaJnxKju6CLHLKcndBqOAboLXbYJBuqz5iYL4ZgD9LGot3hsKtwBrCzlnbz5HpMVRMciZ8xAkk1a9c-FjGGGtRC5J1QHG4wqjtk5KLTHCLW7"
    )

    # Get the venue ID for the given URL slug
    # venue_id = resy.get_resy_venue_id("coqodaq")

    # Get the available time slots for the venue
    time_slots = resy.get_slots("42534", "2024-04-30", 6)

    # Print the available time slots
    # each slot is in the form "rgs://resy/28460/1495834/2/2024-04-30/2024-04-30/21:15:00/6/Dining Table"
    # print only the date and time
    for i, slot in enumerate(time_slots):
        print(f"{i}: {slot.split('/')[-3]}")
        
    if not time_slots:
        return
    slot = int(input("Enter the slot you want to book: "))
    
    if time_slots:
        book_token = resy.get_details(time_slots[slot], "2024-04-30", 6)
        resy.book(book_token)
    
    # time_slots1 = resy.get_slots("76033", "2024-04-26", 6)
    # if time_slots1:
    #     book_token1 = resy.get_details(time_slots1[0], "2024-04-26", 6)
    #     resy.book(book_token1)

    # Get the available config IDs for the time slots
    # book_token = resy.get_details(time_slots[0], "2024-04-15", 6)
    # book_token1 = resy.get_details(time_slots1[0], "2024-04-14", 6)

    # Book a reservation using the first config ID

if __name__ == "__main__":
    go()
