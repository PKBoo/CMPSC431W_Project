from templatesandmoe import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DECIMAL, DateTime


Base = declarative_base()

class Item(Base):
    __tablename__='Items'

    item_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    category_id = Column(Integer)
    name = Column(String)
    price = Column(DECIMAL)
    created_at = Column(DateTime)
