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

    @classmethod
    def get_all(cls):
        item = db.engine.execute(
            """SELECT I.item_id, I.user_id, I.category_id,
            I.name, I.price, I.created_at, 
            C.name AS category_name, U.username AS username
            FROM Items I INNER JOIN Categories C ON I.category_id=C.category_id
            INNER JOIN Users U on I.user_id=U.user_id"""
        ).fetchall()

        return item