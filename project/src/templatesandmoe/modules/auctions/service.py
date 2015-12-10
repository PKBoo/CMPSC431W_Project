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

    def ended(self, service):
        return datetime.now() >= service.end_date

    def mark_bid_as_won(self, bid_id):
        try:
            self.database.execute(text(
                'UPDATE Bids SET winning = 1 WHERE bid_id = :bid_id'
            ), {'bid_id': bid_id})

            self.database.commit()
        except:
            self.database.rollback()
            raise

    def get_services_user_bid_on(self, user_id):
        """
        Gets all services that haven't ended that a user has bid on
        Returns: Array of services

        """

        services = self.database.execute(text(
            'SELECT B.bid_id, B.service_id, I.item_id, I.name, S.end_date, MAX(B.amount) as amount '
            'FROM Bids B '
            'JOIN Services S ON S.service_id = B.service_id '
            'JOIN Items I ON I.item_id = S.item_id '
            'WHERE B.user_id = :user_id AND S.ended = 0 '
            'GROUP BY B.service_id'
        ), {'user_id':user_id})

        return services

    def get_won_bids_by_user(self, user_id):
        bids = self.database.execute(text(
            'SELECT I.item_id, I.name, U.username, B.service_id, B.amount FROM Bids B '
            'JOIN Services S ON S.service_id = B.service_id '
            'JOIN Items I ON I.item_id = S.item_id '
            'JOIN Users U ON I.user_id = U.user_id '
            'WHERE B.winning = 1 AND B.user_id = :user_id'
        ), {'user_id': user_id}).fetchall()

        return bids