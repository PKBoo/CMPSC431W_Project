import schedule
import time
from sqlalchemy.orm import scoped_session, sessionmaker

from flask.ext.sqlalchemy import SQLAlchemy
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.auctions.service import AuctionsService


class AuctionsManager:
    def __init__(self, app, database):

        db = SQLAlchemy(app)
        db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=db.engine))
        self.database = db_session
        self.items = ItemsService(database=db_session)
        self.auctions = AuctionsService(database=db_session)

    def watch_auctions(self):
        """
        Watches for auctions to complete, and marks the highest bid as won
        """

        # Get all services whos ended field is still 0 and their end date has passed
        services = self.items.get_pending_services()

        for service in services:
            try:
                self.items.mark_service_ended(service.service_id)
            except:
                print('failed to update service')

            if service.winning_bid_id is not None:
                self.auctions.mark_bid_as_won(service.winning_bid_id)

        self.database.close()

    def start(self):
        schedule.every(5).seconds.do(self.watch_auctions)
        while True:
            schedule.run_pending()
            time.sleep(1)
