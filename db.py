from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import Base

engine = create_engine('sqlite:///database/characters.db')


Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized with tables: ", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_db()