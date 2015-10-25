import bcrypt
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from templatesandmoe.modules.users.models import User


class UsersService:
    def __init__(self, database):
        self.database = database

    def get_by_id(self, user_id):
        return self.database.query(User).filter(User.user_id == user_id).first()

    def get_all(self):
        return self.database.query(User).all()

    def exists(self, username):
        user = self.database.query(User).filter(User.username == username).first()

        if user is None:
            return False
        else:
            return True

    def delete(self, user):
        self.database.delete(user)
        try:
            self.database.commit()
        except SQLAlchemyError:
            print("SQLAlchemy exception when deleting.")

    def authenticate(self, username, password):
        """ Checks if a username and password is valid

        Args:
            username: Username to check for
            password: Password to check for
        Returns:
            The authenticated user or False if authentication failed
        """

        # First check if the username exists. If it does, check if the password is correct
        user = self.database.execute(text(
            'SELECT * FROM Users WHERE username = :username'
        ), {
            'username': username
        }).fetchone()

        if user is not None:
            submitted_password = password.encode('utf-8')
            user_password = user.password.encode('utf-8')

            if bcrypt.hashpw(submitted_password, user_password) == user_password:
                return user
            else:
                return False
        else:
            return False
