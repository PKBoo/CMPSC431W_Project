import bcrypt
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from templatesandmoe.modules.users.models import User


class UsersService:
    def __init__(self, database):
        self.database = database

    def get_by_id(self, user_id):
        return self.database.query(User).filter(User.user_id == user_id).first()

    def get_by_username(self, username):
        user = self.database.execute(text(
            'SELECT * FROM Users WHERE username = :username'
                ), {
                    'username': username
        }).fetchone()
        return user

    def get_all(self):
        return self.database.query(User).all()

    def get_average_template_rating(self, user_id):
        avg_rating = self.database.execute(text(
            'SELECT amount FROM Ratings R '
            'JOIN Templates T on T.template_id = R.template_id '
            'JOIN Items I on T.item_id = I.item_id Where I.user_id = :user_id'
            ), {'user_id': user_id}).scalar()
        return avg_rating

    def exists(self, username):
        user = self.database.query(User).filter(User.username == username).first()

        if user is None:
            return False
        else:
            return True

    def create(self, username, password, first_name, last_name, email, permissions):
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            permissions=permissions
        )
        new_user.set_password(password)

        self.database.add(new_user)
        self.database.flush()

        try:
            self.database.commit()

            return new_user
        except SQLAlchemyError:
            print('SQLAlchemy exception when creating a new user.')

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
