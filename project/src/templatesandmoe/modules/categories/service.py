from sqlalchemy.sql import text


class CategoriesService:
    def __init__(self, database):
        self.database = database

    def get_children(self, root_category=0):

        query = (
            'SELECT category_id, name '
            'FROM Categories '
            'WHERE parent_id = :category_id'
        )

        tree = self.database.execute(query, { 'category_id': root_category}).fetchall()

        return tree

    def get_root_to_children_path(self, category):

        category_ids = []
        if category is not None and category > 0:
            category_query = (
                'SELECT root.category_id AS root_id, down1.category_id as down1_id, down2.category_id as down2_id '
                'FROM Categories AS root '
                'LEFT OUTER JOIN Categories AS down1 ON down1.parent_id = root.category_id '
                'LEFT OUTER JOIN Categories AS down2 ON down2.parent_id = down1.category_id '
                'WHERE root.category_id = :category_id'
            )

            paths = self.database.execute(text(category_query), {'category_id': category}).fetchall()

            # Query results are all of the category paths that start with 'category'
            # Place each unique category id in a dictionary
            for path in paths:
                if path.root_id not in category_ids and path.root_id is not None:
                    category_ids.append(int(path.root_id))
                if path.down1_id not in category_ids and path.down1_id is not None:
                    category_ids.append(int(path.down1_id))
                if path.down2_id not in category_ids and path.down2_id is not None:
                    category_ids.append(int(path.down2_id))

        return category_ids