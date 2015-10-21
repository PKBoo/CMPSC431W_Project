from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey

Base = declarative_base()

# example query:
# users = db.engine.execute('SELECT * FROM Users')
# for row in users:
#     print(row)

class User(Base):
	__tablename__ = 'Users'

	user_id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String)
	permissions = Column(Integer)
