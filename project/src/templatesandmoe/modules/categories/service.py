from sqlalchemy.sql import text


class CategoriesService:
    def __init__(self, database):
        self.database = database

    def get_children(self, root_category=None):
        """
        SELECT t1.name AS lev1, t2.name as lev2, t3.name as lev3, t4.name as lev4
        FROM category AS t1
        LEFT JOIN category AS t2 ON t2.parent = t1.category_id
        LEFT JOIN category AS t3 ON t3.parent = t2.category_id
        LEFT JOIN category AS t4 ON t4.parent = t3.category_id
        WHERE t1.name = 'ELECTRONICS';
        :param root_category:
        :return:
        """

        query = (
            'SELECT category_id, name '
            'FROM Categories '
        )

        if root_category is None:
            query += ('WHERE parent_id = 0')
        else:
            query += ('WHERE parent_id = :category_id')

        tree = self.database.execute(query, { 'category_id': root_category}).fetchall()

        return tree