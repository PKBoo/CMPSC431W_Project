from datetime import datetime
from sqlalchemy.sql import text
from templatesandmoe.modules.core.database import insert

class AuctionsService:
    def __init__(self, database):
        self.database = database

    def get_bids_for_service(self, service_id):
        query = (
            'SELECT U.user_id, U.username, B.created_at, B.amount '
            'FROM Bids B '
            'JOIN Users U ON U.user_id = B.user_id '
            'WHERE B.service_id = :service_id '
            'ORDER BY B.created_at DESC'
        )

        bids = self.database.execute(text(query), {'service_id': service_id}).fetchall()

        return bids

    def get_highest_bid(self, service_id):
        query = (
            'SELECT B.user_id, B.amount '
            'FROM Bids B '
            'WHERE B.service_id = :service_id '
            'ORDER BY B.amount DESC LIMIT 1'
        )

        bid = self.database.execute(text(query), {'service_id': service_id}).fetchone()

        return bid

    def place_bid(self, service_id, user_id, amount):

        try:
            bid = insert(self.database, 'Bids', [
                ('service_id', service_id),
                ('user_id', user_id),
                ('amount', amount),
                ('created_at', datetime.now().isoformat())
            ])

            self.database.commit()

            return bid
        except:
            self.database.rollback()
            raise