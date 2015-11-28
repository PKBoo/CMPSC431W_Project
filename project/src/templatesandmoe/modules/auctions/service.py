from sqlalchemy.sql import text


class AuctionsService:
    def __init__(self, database):
        self.database = database