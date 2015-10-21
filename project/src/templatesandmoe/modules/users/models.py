import bcrypt
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from templatesandmoe import db

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

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @classmethod
    def authenticate(cls, username, password):
        """ Checks if a username and password is valid

        Args:
            username: Username to check for
            password: Password to check for
        Returns:
            The authenticated user or False if authentication failed
        """

        # First check if the username exists. If it does, check if the password is correct
        user = db.engine.execute(text(
            'SELECT * FROM Users WHERE username = :username'
        ), username=username).fetchone()

        if user is not None:
            submitted_password = password.encode('utf-8')
            user_password = user.password.encode('utf-8')

            if bcrypt.hashpw(submitted_password, user_password) == user_password:
                return user
            else:
                return False
        else:
            return False
