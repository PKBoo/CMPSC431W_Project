from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from templatesandmoe import db, db_session

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    permissions = Column(Integer)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def create(self):
        db_session.add(self)
        db_session.commit()

        return self

    def save(self):
        db_session.add(self)
        db_session.commit()

        return self
