import datetime
from sqlalchemy.sql import text
from templatesandmoe.modules.categories.service import CategoriesService
from templatesandmoe.modules.core.database import insert


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
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.description, '
                    'I.created_at, C.name AS category_name, C.category_id AS category_id, U.user_id, U.username '
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
            'JOIN Users U ON U.user_id = I.user_id '
        )
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

        query = (
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
            'C.name AS category_name, U.username, '
            # Want to calculate average rating for each template
            '(SELECT AVG(R.amount) '
            'FROM Ratings R '
            'WHERE R.template_id = T.template_id) as rating '
        ) + query

        query += (
            'ORDER BY rating DESC '
            'LIMIT ' + limit + ' OFFSET ' + offset
        )

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

    def get_latest_templates(self, limit):
        templates = self.database.execute(text(
            'SELECT T.template_id, I.item_id, T.file_path, I.category_id, I.name, I.price, I.created_at, '
                'U.username, U.user_id '
            'FROM Templates T '
            'JOIN Items I ON I.item_id = T.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'ORDER BY created_at DESC '
            'LIMIT :limit'
        ), {'limit': limit})

        return templates

    def add_template(self, user_id, name, price, description, category, tags=[]):
        try:
            item = insert(self.database, 'Items', [
                ('user_id', user_id),
                ('category_id', category),
                ('name', name),
                ('price', price),
                ('created_at', datetime.datetime.now().isoformat()),
                ('description', description)
            ])

            item_id = item.lastrowid

            template = insert(self.database, 'Templates', [
                ('item_id', item_id),
                ('file_path', '')
            ])

            self.database.commit()

            return item_id
        except:
            self.database.rollback()
            raise

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

    def get_service_by_id(self, item_id):
        query = (
            'SELECT S.service_id, S.end_date, I.item_id, I.name, I.price as start_price, I.created_at, '
            'I.description, U.user_id, U.username, '
            '(SELECT MAX(B.amount) FROM Bids B WHERE B.service_id = S.service_id) AS highest_bid, '
            '(SELECT COUNT(*) FROM Bids B Where B.service_id = S.service_id) AS bids '
            'FROM Services S '
            'JOIN Items I ON I.item_id = S.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'WHERE I.item_id = :item_id'
        )

        service = self.database.execute(text(query), {'item_id': item_id}).fetchone()

        return service

    def get_filtered_services(self, page=1, services_per_page=16):
        query = (
            'SELECT S.service_id, S.end_date, I.item_id, I.name, I.price as start_price, I.created_at, '
            'U.user_id, U.username, '
            '(SELECT MAX(B.amount) FROM Bids B WHERE B.service_id = S.service_id) AS highest_bid, '
            '(SELECT COUNT(*) FROM Bids B Where B.service_id = S.service_id) AS bids '
            'FROM Services S '
            'JOIN Items I ON I.item_id = S.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'WHERE :current_datetime < S.end_date '
            'ORDER BY S.end_date ASC '
        )
        count_query = (
            'SELECT COUNT(S.service_id)'
            'FROM Services S '
            'JOIN Items I ON I.item_id = S.item_id '
            'JOIN Users U ON U.user_id = I.user_id '
            'WHERE :current_datetime < S.end_date '
        )

        params = {
            'current_datetime': datetime.datetime.now().isoformat()
        }
        where_clauses = []

        count = self.database.execute(text(count_query), params).scalar()

        page -= 1
        limit = str((page * services_per_page) + services_per_page)
        offset = str(page * services_per_page)

        query += (
            'LIMIT ' + limit + ' OFFSET ' + offset
        )

        services = self.database.execute(text(query), params).fetchall()

        return [services, int(count)]

    def get_pending_services(self):
        query = (
            'SELECT S.service_id, '
            '(SELECT bid_id FROM Bids WHERE service_id = S.service_id ORDER BY amount DESC LIMIT 1) as winning_bid_id '
            'FROM Services S '
            'WHERE :current_datetime >= S.end_date AND S.ended = 0'
        )

        services = self.database.execute(text(query), {
            'current_datetime': datetime.datetime.now().isoformat()
        }).fetchall()

        return services

    def add_service(self, user_id, name, start_price, description, duration):
        try:
            item = insert(self.database, 'Items', [
                ('user_id', user_id),
                ('name', name),
                ('price', start_price),
                ('created_at', datetime.datetime.now().isoformat()),
                ('description', description)
            ])

            item_id = item.lastrowid
            end_date = datetime.datetime.now() + datetime.timedelta(days=duration)

            service = insert(self.database, 'Services', [
                ('item_id', item_id),
                ('end_date', end_date.isoformat())
            ])

            self.database.commit()

            return item_id
        except:
            self.database.rollback()
            raise

    def mark_service_ended(self, service_id):
        try:
            query = (
                'UPDATE Services SET ended = 1 WHERE service_id = :service_id'
            )
            self.database.execute(text(query), {'service_id': service_id})
            self.database.commit()
        except:
            self.database.rollback()
            raise
