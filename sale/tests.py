from django.test import TestCase
from bid import Bid
# Create your tests here.

class BiddingTestCase(TestCase):
    def placeBidTest(self):
        sale = Sale(1, 55)
        bid = Bid(sale)
        u1 = User(1)
        u2 = User(2)
        bid.place_bid(u1, bidPrice=10)
        bid.place_bid(u2, bidPrice=100)


class User():
    def __init__(self):
        self.pk = pk

class Sale():
    def __init__(self, pk, price):
        self.pk = pk
        self.price = price
