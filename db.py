from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

engine = create_engine('sqlite:///database/characters.db')


Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized with tables: ", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_db()