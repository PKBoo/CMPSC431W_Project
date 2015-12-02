import datetime
from sqlalchemy.sql import text
from templatesandmoe.modules.core.database import insert

class RatingsService:
    def __init__(self, database):
        self.database = database

    def get_average_by_template_id(self, template_id):
        rating = self.database.execute(text(
            'SELECT AVG(amount) FROM Ratings WHERE template_id = :template_id'
        ), {'template_id': template_id}).scalar()

        # Round to nearest 0.5
        if rating:
            return round(rating*2)/2
        else:
            return None

    def get_rating_for_template_by_user(self, template_id, user_id):
        rating = self.database.execute(text(
            'SELECT amount FROM  Ratings WHERE template_id = :template_id AND user_id = :user_id'
        ), {
            'template_id': template_id,
            'user_id': user_id
        }).scalar()

        return rating

    def exists(self, template_id, user_id):
        rating = self.database.execute(text(
            'SELECT * FROM Ratings WHERE template_id = :template_id AND user_id = :user_id'
        ), {
            'template_id': template_id,
            'user_id': user_id
        }).fetchone()

        return rating

    def add_rating(self, template_id, user_id, amount):
        try:
            transaction = insert(self.database, 'Ratings', [
                ('template_id', template_id),
                ('user_id', user_id),
                ('amount', amount),
                ('created_at', datetime.datetime.now().isoformat())
            ])
            self.database.commit()
        except:
            self.database.rollback()

    def update_rating(self, template_id, user_id, amount):
        try:
            transaction = self.database.execute(text(
                'UPDATE Ratings SET amount = :amount, created_at = NOW() WHERE template_id = :template_id AND user_id = :user_id'
            ), {
                'amount': amount,
                'template_id': template_id,
                'user_id': user_id
            })

            self.database.commit()
        except:
            self.database.rollback()
