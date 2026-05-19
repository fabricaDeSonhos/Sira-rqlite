import datetime

from colour import Color
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models.booking import BookingTable, CategoryTable

engine = create_engine("sqlite:///fabtec.db", echo=False)

def add_category(name: str, color: Color):
    with Session(engine) as session:
        category = CategoryTable(name=name, color=color)
        session.add(category)
        session.commit()

def get_category(name: str = None, color: Color = None):
    with Session(engine) as session:
        query = select(CategoryTable)
        if name:
            query = query.where(CategoryTable.name == name)
        if color:
            query = query.where(CategoryTable.color == color)
        return session.execute(query).scalars().all()

def add_booking(
        user: str, 
        artifact: str, 
        date: datetime.date, 
        start_time: datetime.time, 
        end_time: datetime.time, 
        purpose: str, 
        category_name: str, 
        observations: str = None
    ):
    with Session(engine) as session:
        if get_booking(user=user, artifact=artifact, date=date, start_time=start_time, end_time=end_time, category_name=category_name, active=True):
            raise ValueError("Booking already exists for the given parameters.")
        
        category = session.execute(select(CategoryTable).where(CategoryTable.name == category_name)).scalar_one()
        booking = BookingTable(
            user=user,
            artifact=artifact,
            date=date,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            category=category.id,
            observations=observations,
            created_at=datetime.datetime.now()
        )
        session.add(booking)
        session.commit()

def get_booking(
        user: str = None, 
        artifact: str = None, 
        date: datetime.date = None, 
        start_time: datetime.time = None, 
        end_time: datetime.time = None, 
        purpose: str = None, 
        category_name: str = None, 
        observations: str = None,
        active: bool = None
    ):
    with Session(engine) as session:
        query = select(BookingTable)
        if user:
            query = query.where(BookingTable.user == user)
        if artifact:
            query = query.where(BookingTable.artifact == artifact)
        if date:
            query = query.where(BookingTable.date == date)
        if start_time:
            query = query.where(BookingTable.start_time == start_time)
        if end_time:
            query = query.where(BookingTable.end_time == end_time)
        if purpose:
            query = query.where(BookingTable.purpose == purpose)
        if category_name:
            category = session.execute(select(CategoryTable).where(CategoryTable.name == category_name)).scalar_one()
            query = query.where(BookingTable.category == category.id)
        if observations:
            query = query.where(BookingTable.observations.contains(observations))
        if active is not None:
            query = query.where(BookingTable.active == active)
        
        return session.execute(query).scalars().all()

def batch_add_booking(
        user: str, 
        artifact: str, 
        date_list: list[datetime.date], 
        start_time: datetime.time, 
        end_time: datetime.time, 
        purpose: str, 
        category_name: str, 
        observations: str = None
    ):
    with Session(engine) as session:
        category = session.execute(select(CategoryTable).where(CategoryTable.name == category_name)).scalar_one()
        batch_id = f"{user}_{artifact}_{datetime.datetime.now().isoformat()}"
        for date in date_list:
            if get_booking(user=user, artifact=artifact, date=date, start_time=start_time, end_time=end_time, category_name=category_name, active=True):
                print(f"Booking already exists for the given parameters on date {date}.")
                continue

            booking = BookingTable(
                user=user,
                artifact=artifact,
                date=date,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                category=category.id,
                observations=observations,
                created_at=datetime.datetime.now(),
                batch_id=batch_id
            )
            session.add(booking)
        session.commit()
        return batch_id

def cancel_booking(booking_id: int, canceler_user: str):
    with Session(engine) as session:
        booking = session.get(BookingTable, booking_id)
        if booking:
            booking.active = False
            booking.canceler_user = canceler_user
            session.commit()
            return True
        return False