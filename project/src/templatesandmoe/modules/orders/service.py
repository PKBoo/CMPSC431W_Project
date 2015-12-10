from sqlalchemy.sql import text
from templatesandmoe.modules.core.database import insert
import datetime

class OrdersService:
    def __init__(self, database):
        self.database = database

    def get_order_by_id(self, transaction_id):
        transaction = self.database.execute(text(
            'SELECT T.transaction_id, T.user_id, T.created_at, I.item_id, I.name, I.price, '
                'T.card_name, T.card_number, SUM(I.price) as total '
            'FROM Transactions T '
            'JOIN Transaction_Items TI ON T.transaction_id = TI.transaction_id '
            'JOIN Items I ON TI.item_id = I.item_id '
            'WHERE T.transaction_id = :transaction_id'
        ), {
            'transaction_id': transaction_id
        }).fetchall()

        return transaction

    def create_order(self, user_id, card_payment, items):
        try:
            transaction = insert(self.database, 'Transactions', [
                ('user_id', user_id),
                ('created_at', datetime.datetime.now().isoformat()),
                ('card_number', card_payment.number),
                ('card_name', card_payment.name),
                ('card_expiration', card_payment.expiration.isoformat()),
                ('card_cvc', card_payment.cvc)
            ])

            transaction_id = transaction.lastrowid

            for item_id in items:
                insert(self.database, 'Transaction_Items', [
                    ('transaction_id', transaction_id),
                    ('item_id', item_id)
                ])

            self.database.commit()

            return transaction_id

        except:
            self.database.rollback()
            raise

    def get_orders_by_user(self, user_id):
        orders = self.database.execute(text(
            'SELECT T.transaction_id, T.created_at, I.item_id, I.name, I.price, '
				'('
					'SELECT SUM(I2.price) as total FROM Transactions T2 '
					'JOIN Transaction_Items TI2 ON TI2.transaction_id = T2.transaction_id '
                    'JOIN Items I2 ON I2.item_id = TI2.item_id '
                    'WHERE T2.transaction_id = T.transaction_id '
                ') as total '
			'FROM Transactions T '
            'JOIN Transaction_Items TI ON TI.transaction_id = T.transaction_id '
            'JOIN Items I ON I.item_id = TI.item_id '
            'WHERE T.user_id = :user_id '
        ), {'user_id': user_id}).fetchall()

        return_orders = {}
        for order in orders:
            if order.transaction_id in return_orders:
                return_orders[order.transaction_id]['items'].append(order)
            else:
                return_orders[order.transaction_id] = {
                    'transaction_id': order.transaction_id,
                    'created_at': order.created_at,
                    'total': order.total,
                    'items': [order]
                }

        return return_orders
