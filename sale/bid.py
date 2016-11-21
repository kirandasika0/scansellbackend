from utils import MaxPQ
class Bid():
    def __init__(self, saleIn):
        self.sale = saleIn
        self.cacheKey = str(self.sale.pk) + "_bid"
        self.bidData = {
            'sale_id': self.sale.pk,
            'sale_buy_now': self.sale.price
        }
    
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
        
        if "bidders" not in self.bidData.keys():
            # This is the first bid for this sale
            self.bidData['highest_bidder'] = str(user.pk) + "-" + str(bidPrice)
            self.bidData['bidders'] = [str(user.pk) + "-" + str(bidPrice)]
            self.serialize()
            return True
        
        
        for bidder in self.bidData['bidders']:
            userId, userBidPrice = bidder.split('-')
            if bidPrice > userBidPrice:
                self.bidData['highest_bidder'] = str(user.pk) + "-" + str(bidPrice)
                
        
    
    def delete_bid(self, user):
        pass
    
    def serialize(self):
        pass
    
    def deserialize(self):
        pass
    
    def hasUserBid(self, user):
        pass
    