from utils import MaxPQ, MemcacheWrapper
class Bid():
    def __init__(self, saleIn=None):
        if saleIn is not None:
            self.sale = saleIn
            self.cacheKey = str(self.sale.pk) + "_bid"
            self.bidData = {
                'sale_id': self.sale.pk,
                'sale_buy_now': self.sale.price
            }
        self.bidderPQ = MaxPQ()

    def place_bid(self, user, bidPrice=1):
        """
        This method takes a user and bidPrice and checks if its the highest bid.
        Then adds it to the bid data and serializes and sends a notification to
        the required user

        Arguments:
        user: a instance of the User model
        bidPirce: an int depicting the bidPrice

        :return: boolean
        """
        bidUsr = BidUser(user.pk, bidPrice)

        if "highest_bidder" not in self.bidData.keys():
            # This is the first bid for this sale
            self.bidData['highest_bidder'] = bidUsr.serialize()
            self.bidderPQ.enqueue(bidUsr)
            return True

        # Checking if the max in the bidderPQ is less than the argument price
        maxBidderPQPrice = self.bidderPQ.peek().bidPrice
        if maxBidderPQPrice < bidPrice:
            # new price is the highest price
            self.bidData['highest_bidder'] = bidUsr.serialize()
            self.bidderPQ.enqueue(bidUsr)
            return True

    def serialize(self, mc):
        # serialize the priority queue
        pqList = []
        n = self.bidderPQ.max
        while n is not None:
            userStr = str(n.element.pk) + "-" + str(n.element.bidPrice)
            pqList.append(userStr)
            n = n.next
        self.bidData['bidders'] = pqList
        return mc.set_key_value(self.cacheKey, self.bidData)

    def deserialize(self, cacheKey, mc):
        self.bidData = mc.get_val(cacheKey)
        for user in self.bidData['bidders']:
            userId, bidPrice = user.split('-')
            self.bidderPQ.enqueue(BidUser(userId, bidPrice))
        self.cacheKey = cacheKey
        del self.bidData['bidders']
        return True



class BidUser():
    def __init__(self, pk, bidPrice):
        self.pk = int(pk)
        self.bidPrice = int(bidPrice)

    def getPk(self):
        return self.pk

    def getBidPrice(self):
        return self.bidPrice

    def serialize(self):
        return str(self.pk) + "-" + str(self.bidPrice)

    def comparePriceTo(self, that):
        if self.bidPrice > that.bidPrice:
            return 1
        elif self.bidPrice < that.bidPrice:
            return -1
        else:
            return 0
