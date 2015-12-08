from sqlalchemy.sql import text
from templatesandmoe.modules.core.database import insert


class TagsService:
    def __init__(self, database):
        self.database = database

    def get_all(self):
        tags = self.database.execute('SELECT * FROM Tags ORDER BY name').fetchall()

        return tags

    def exists(self, tag):
        tag = self.database.execute('SELECT * FROM Tags WHERE name = :name', {'name': tag})

        return tag is not None

    def get_by_name(self, tag):
        tag = self.database.execute('SELECT * FROM Tags WHERE name = :name', {'name': tag}).fetchone()

        return tag

    def get_tags_for_item(self, item_id):
        tags = self.database.execute(text(
            'SELECT T.tag_id, T.name FROM Item_Tags IT '
            'JOIN Tags T ON T.tag_id = IT.tag_id '
            'WHERE IT.item_id = :item_id'
        ), {'item_id': item_id}).fetchall()

        return tags

    def create_custom_tags_for_item(self, tags, item_id):
        for tag in tags:
            try:
                existing_tag = self.get_by_name(tag)
                if existing_tag is None:
                    # Insert the new tag, then insert into Item_tags using the lastinsertid
                    result = insert(self.database, 'Tags', [
                        ('name', tag)
                    ])

                    new_tag_id = result.lastrowid
                else:
                    new_tag_id = existing_tag.tag_id

                insert(self.database, 'Item_Tags', [
                    ('item_id', item_id),
                    ('tag_id', new_tag_id)
                ])

                self.database.commit()

            except Exception as e:
                print(e)
                self.database.rollback()

    def add_tags_to_item(self, tags, item_id):
        for tag in tags:
            try:
                insert(self.database, 'Item_Tags', [
                    ('item_id', item_id),
                    ('tag_id', tag)
                ])

                self.database.commit()
            except Exception as e:
                print(e)
                self.database.rollback()


