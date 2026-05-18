from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.base import create_db, drop_db
from models.booking import CategoryTable

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

if __name__ == "__main__":
    main()