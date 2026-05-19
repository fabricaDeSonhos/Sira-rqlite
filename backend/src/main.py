import datetime

from colour import Color

from database.base import create_db, drop_db
from database.session import add_booking, add_category, get_booking, get_category

def main():
    drop_db()
    create_db()
    add_category("Test Category1", Color("blue"))
    add_category("Test Category2", Color("green"))
    add_booking(
        user="Hylson",
        artifact="Sala C16",
        date=datetime.date.today(),
        start_time=datetime.time(13, 0),
        end_time=datetime.time(17, 0),
        purpose="FabTec",
        category_name="Test Category1",
        observations="Test booking"
    )

    bookings = get_booking(user="Hylson", artifact="Sala C16")
    for booking in bookings:
        print(f"{booking.user} {booking.artifact}: {booking.date} {booking.start_time} - {booking.end_time} \nPurpose: {booking.purpose} \nCategory: {booking.category} \nObservations: {booking.observations}")

if __name__ == "__main__":
    main()