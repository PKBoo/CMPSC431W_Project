from sqlalchemy.sql import text
from templatesandmoe.modules.categories.service import CategoriesService


class ItemsService:
    def __init__(self, database):
        self.database = database
        self.categories = CategoriesService(database=database)

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
                    'C.name AS category_name, C.category_id AS category_id, U.user_id, U.username '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Categories C ON I.category_id = C.category_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'WHERE I.item_id = :item_id'
        ), {'item_id': item_id}).fetchone()

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

    def get_filtered_templates(self, page=1, templates_per_page=16, price_start=None, price_end=None, category=None, search=None):

        query = (
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Categories C ON I.category_id = C.category_id '
            'JOIN Users U ON U.user_id = I.user_id ')
        params = {}
        where_clauses = []

        # Build where clause by appending each condition to a list, then joining at the end.

        if category is not None and category > 0:
            # Get a list of category ids to search in
            # We need to do this to show all items that belong to any subcategories
            # eg. When looking at 'Resume' we need to also show items that belong to the subcategory 'CV'
            category_ids = self.categories.get_root_to_children_path(category)
            where_clauses.append('I.category_id IN :category_ids ')
            params['category_ids'] = category_ids

        if price_start:
            where_clauses.append('I.price >= :price_start')
            params['price_start'] = float(price_start)

        if price_end:
            where_clauses.append('I.price <= :price_end')
            params['price_end'] = float(price_end)

        if search:
            where_clauses.append('I.name LIKE :keywords')
            params['keywords'] = '%' + search + '%'

        if len(where_clauses) > 0:
            where_clauses[0] = 'WHERE ' + where_clauses[0]

        final_where_clause = ' AND '.join(where_clauses) + ' '
        query += final_where_clause

        page -= 1
        limit = str((page * templates_per_page) + templates_per_page)
        offset = str(page * templates_per_page)

        # Need to also get the total row count for filtered results for pagination
        count_query = 'SELECT COUNT(T.template_id) ' + query
        count = self.database.execute(text(count_query), params).scalar()

        query = ('SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                'C.name AS category_name, U.username ') + query

        query += ('LIMIT ' + limit + ' OFFSET ' + offset)

        templates = self.database.execute(text(query), params).fetchall()

        return [templates, int(count)]

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
