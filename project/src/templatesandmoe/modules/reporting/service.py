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

    def items_sales_report(self, period='All', item_id=None):
        query = ('SELECT I.item_id, I.name, U.username, COUNT(TI.item_id) as sales, SUM(I.price) as revenue '
                 'FROM Templates T '
                 'JOIN Items I ON I.item_id = T.item_id '
                 'JOIN Users U ON U.user_id = I.user_id '
                 'JOIN Transaction_Items TI ON TI.item_id = I.item_id '
                 'JOIN Transactions TR ON TI.transaction_id = TR.transaction_id '
                 )
        params = {}

        if item_id is not None:
            query += 'HAVING I.item_id = :item_id'
            params['item_id'] = item_id

        # Want to get the entirety of today
        time = datetime.time(0, 0)
        date = datetime.datetime.now().date()
        today = datetime.datetime.combine(date, time) + datetime.timedelta(seconds=59, minutes=59, hours=23)

        if period == 'today':
            start_date = datetime.datetime.combine(date, time)
            end_date = today
        elif period == 'week':
            end_date = today
            start_date = today - datetime.timedelta(weeks=1)
        elif period == 'month':
            end_date = today
            start_date = today - datetime.timedelta(weeks=4)
        elif period == 'year':
            end_date = today
            start_date = today - datetime.timedelta(weeks=52)
        else:
            start_date = None
            end_date = None

        if start_date and end_date:
            query += 'WHERE TR.created_at >= :start_date AND TR.created_at < :end_date '
            params['start_date'] = start_date.isoformat()
            params['end_date'] = end_date.isoformat()

        query += 'GROUP BY I.item_id'

        items = self.database.execute(text(query), params).fetchall()

        return items

    def item_sales_report_for_user(self, user_id):
            report = self.database.execute(text(
                'SELECT I.item_id, I.name, U.username, COUNT(TI.item_id) as sales, SUM(I.price) as revenue '
                'FROM Templates T '
                'JOIN Items I ON I.item_id = T.item_id '
                'JOIN Users U ON U.user_id = I.user_id '
                'JOIN Transaction_Items TI ON TI.item_id = I.item_id '
                'JOIN Transactions TR ON TI.transaction_id = TR.transaction_id '
                'WHERE I.user_id = :user_id'
            ), {'user_id': user_id}).fetchall()

            return report