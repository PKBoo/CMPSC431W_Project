import bcrypt
from sqlalchemy.sql import text
from templatesandmoe import db


class AuthRepository:

    def authenticate(self, username, password):
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

        if len(user) > 0:
            submitted_password = password.encode('utf-8')
            user_password = user.password.encode('utf-8')

            if bcrypt.hashpw(submitted_password, user_password) == user_password:
                return user
            else:
                return False
        else:
            return False

