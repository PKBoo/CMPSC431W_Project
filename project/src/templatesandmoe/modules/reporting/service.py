import datetime
from sqlalchemy.sql import text


class ReportingService:
    def __init__(self, database):
        self.database = database

    def total_revenue(self):
        total = self.database.execute((text(
            'SELECT SUM(I.price) as total FROM Transaction_Items TI '
            'JOIN Items I ON I.item_id = TI.item_id'
        ))).scalar()

        return total

    def total_transactions(self):
        total = self.database.execute(
            'SELECT COUNT(*) as total FROM Transactions'
        ).scalar()

        return total

    def total_won_bids(self):
        total = self.database.execute(
            'SELECT COUNT(*) as total FROM Bids WHERE Bids.winning = 1'
        ).scalar()

        return total

    def items_sales_report(self, item_id=None):
        query = ('SELECT I.item_id, I.name, U.username, COUNT(TI.item_id) as sales, SUM(I.price) as revenue '
                'FROM Templates T '
                'JOIN Items I ON I.item_id = T.item_id '
                'JOIN Users U ON U.user_id = I.user_id '
                'JOIN Transaction_Items TI ON TI.item_id = I.item_id '
                'GROUP BY I.item_id ')
        params = {}

        if item_id is not None:
            query += 'HAVING I.item_id = :item_id'
            params['item_id'] = item_id

        items = self.database.execute(text(query), params).fetchall()

        return items
