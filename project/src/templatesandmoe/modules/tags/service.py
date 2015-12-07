from sqlalchemy.sql import text
from templatesandmoe.modules.core.database import insert


class TagsService:
    def __init__(self, database):
        self.database = database

    def get_all(self):
        tags = self.database.execute('SELECT * FROM Tags ORDER BY name').fetchall()

        return tags