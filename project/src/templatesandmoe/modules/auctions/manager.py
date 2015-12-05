import schedule
import time

from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.auctions.service import AuctionsService

class AuctionsManager:
    def __init__(self, database):
        self.database = database
        self.items = ItemsService(database=database)
        self.auctions = AuctionsService(database=database)

    def watch_auctions(self):
        """
        Watches for auctions to complete, and marks the highest bid as won
        """
        print('Checking for any pending auctions')

        # Get all services whos ended field is still 0 and their end date has passed
        services = self.items.get_pending_services()
        for service in services:
            print('Marking ' + str(service.service_id))
            try:
                self.items.mark_service_ended(service.service_id)
            except:
                print('failed to update service')
            if service.winning_bid_id is None:
                print('Found winnning bid for ' + str(service.service_id))
                print(service.winning_bid_id)
                self.auctions.mark_bid_as_won(service.winning_bid_id)


    def start(self):
        schedule.every(5).seconds.do(self.watch_auctions)
        while True:
            schedule.run_pending()
            time.sleep(1)
