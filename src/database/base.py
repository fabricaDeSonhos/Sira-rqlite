from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def create_db(engine):
    Base.metadata.create_all(engine)

def drop_db(engine):
    Base.metadata.drop_all(engine)