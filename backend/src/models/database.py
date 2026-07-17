from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite:///fabtec.db", echo=False)

class Base(DeclarativeBase):
    """ Classe base para os modelos do SQLAlchemy. """
    pass