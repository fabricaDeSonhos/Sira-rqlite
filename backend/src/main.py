import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.base import create_db, drop_db
from models.booking import BookingTable, CategoryTable

def main():
    engine = create_engine("sqlite:///fabtec.db", echo=False)
    drop_db(engine)
    create_db(engine)
    
    categories = {
        CategoryTable(name="Veículo do campus", color="#ff5733"),
        CategoryTable(name="Sala de aula", color="#33ff57"),
        CategoryTable(name="Laboratório de informática", color="#3357ff"),
    }

    with Session(engine) as session:
        session.add_all(categories)
        session.commit()

        sel = select(CategoryTable)
        categories_query = session.execute(sel).scalars().all()
        for category in categories_query:
            print(category.name, category.color)

        sel = select(CategoryTable).where(CategoryTable.name == "Laboratório de informática")
        target_category = session.execute(sel).scalars().first()
        bookings = {
            BookingTable(
                user="Hylson",
                artifact="Sala C16",
                date=datetime.date.today(),
                start_time=datetime.time(13, 0),
                end_time=datetime.time(17, 0),
                purpose="Fabrica de software",
                category=target_category.id,
                observations="Levar notebook",
                created_at=datetime.datetime.now()
            ),
            BookingTable(
                user="Ladeira",
                artifact="Sala C14",
                date=datetime.date.today(),
                start_time=datetime.time(13, 0),
                end_time=datetime.time(17, 0),
                purpose="TCC",
                category=target_category.id,
                created_at=datetime.datetime.now()
            )
        }

        session.add_all(bookings)
        session.commit()

        sel = select(BookingTable)
        bookings_query = session.execute(sel).scalars().all()
        for booking in bookings_query:
            print(booking.user, booking.artifact, booking.purpose)

if __name__ == "__main__":
    main()