from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from templatesandmoe.modules.items.models import Item


class ItemsService:
    def __init__(self, database):
        self.database = database

    def get_all(self):
        items = self.database.execute(
            'SELECT I.item_id, I.user_id, I.category_id,'
                    'I.name, I.price, I.created_at,'
                    'C.name AS category_name, U.username AS username '
            'FROM Items I '
            'LEFT JOIN Categories C ON I.category_id=C.category_id '
            'INNER JOIN Users U on I.user_id=U.user_id'
        ).fetchall()

        return items
