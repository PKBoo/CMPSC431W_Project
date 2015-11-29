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

    def get_template_by_id(self, item_id):
        template = self.database.execute(text(
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                    'U.user_id, U.username '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'WHERE I.item_id = :item_id'
        ), { 'item_id': item_id }).fetchone()

        return template

    def get_all_templates(self):
        templates = self.database.execute(
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                'C.name AS category_name, U.username '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Categories C ON I.category_id = C.category_id '
            'JOIN Users U ON U.user_id = I.user_id '
        )

        return templates

    def templates_count(self):
        count = self.database.execute(
            'SELECT COUNT(*) FROM Templates'
        ).scalar()

        return count

    def get_filtered_templates(self, page=1, templates_per_page=16, category=None, keywords=None):
        query =  (
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                'C.name AS category_name, U.username '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Categories C ON I.category_id = C.category_id '
            'JOIN Users U ON U.user_id = I.user_id ')
        params = {}

        if category is not None and category > 0:
            query += ('WHERE I.category_id = :category_id ')
            params['category_id'] = category

        page -= 1
        limit = str((page * templates_per_page) + templates_per_page)
        offset = str(page * templates_per_page)

        query += ('LIMIT ' + limit + ' OFFSET ' + offset)


        templates = self.database.execute(text(query), params).fetchall()

        return templates

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

    def get_all_services(self):
        services = self.database.execute(
            'SELECT S.service_id, I.item_id, S.end_date, I.name, I.price, I.created_at, U.username '
            'FROM Services S '
            'JOIN Items I ON I.item_id = S.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
        )

        return services

    def get_services_by_user_id(self, user_id):
        services = self.database.execute(text(
            'SELECT S.service_id, I.item_id, S.end_date, I.name, I.price, I.created_at '
            'FROM Services S '
            'JOIN Items I ON I.item_id = S.item_id '
            'WHERE I.user_id = :user_id'
        ), {'user_id': user_id})

        return services

    def get_latest_templates(self, limit):
        templates = self.database.execute(text(
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                'U.username, U.user_id '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'ORDER BY created_at DESC '
            'LIMIT :limit'
        ), { 'limit': limit})

        return templates
