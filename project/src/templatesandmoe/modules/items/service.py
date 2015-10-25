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
            'LEFT JOIN Categories C ON I.category_id = C.category_id '
            'INNER JOIN Users U ON I.user_id = U.user_id'
        ).fetchall()

        return items

    def get_templates_by_user_id(self, user_id):
        templates = self.database.execute(text(
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                'C.name AS category_name '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Categories C ON I.category_id = C.category_id '
            'WHERE I.user_id = :user_id'
        ), {'user_id': user_id})

        return templates

    def get_services_by_user_id(self, user_id):
        services = self.database.execute(text(
            'SELECT S.service_id, I.item_id, S.end_date, I.name, I.price, I.created_at '
            'FROM Services S '
            'JOIN Items I ON I.item_id = S.item_id '
            'WHERE I.user_id = :user_id'
        ), {'user_id': user_id})

        return services
