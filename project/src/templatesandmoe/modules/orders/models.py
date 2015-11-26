import datetime

class CardPayment:
    def __init__(self, name, number, expiration_month, expiration_year, cvc):
        self.name = name
        self.number = number
        self.expiration = datetime.date(expiration_year, month=expiration_month, day=1)
        self.cvc = cvc
