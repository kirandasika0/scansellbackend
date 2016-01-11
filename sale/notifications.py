import json, time
from .models import SaleNotification, Sale
###########################################
#All imports above this comment
'''
Defining all the notification types

Notification Type 1 - Request to the seller from a random buyer/user
    *This type of notification only comes once per product and per buyer
    *If the seller accepts this request then his information is passed to the buyer
    *will be deleted after the seller accpepts the request.
    
Notification Type 2 - A Notification to tell the buyer about the seller's information
    *This notification only appears when the seller has accpeted the 1st notification
    type
    *This notification will remain until the seller has marked the product as sold.
    
Notification Type 3 - Warning to the seller telling him that his pictures are shit.
    *This notification will be sent to the user only when the buyer thinks his pics
    are sketchy
    
'''


class Notification:
    #Constructer method to take input the 
    def __init__(self, notif_type, data):
        self.notif_type = notif_type
        self.data = data
        
        
    def set_notif_type_1(self):
        ''' Setter method to set the notif 1 type in the database
        make sure the type and the data go in correct '''
        #the data that has come form client side
        response = self.data
        #buyer_id - the current user sending the request
        #buyer_username  - the current username sending the request
        #seller_id - the user who uploaded the product
        #seller_username - the username who uploaded the product
        notif_data = json.dumps({'type': 1, 'buyer_id': response["buyer_id"],
                    'buyer_username': response["buyer_username"],
                    'buyer_username': response["buyer_username"]})
                    
        #inserting data into the database
        SaleNotification.objects.create(notif_type=1, user_id=response["seller_id"],
                                        user_name = response["seller_username"],
                                        sale = Sale.objects.get(pk=int(response["sale_id"])),
                                        notif_data=notif_data)
                                        
        return json.dumps({'response': 'true'})
        
    def set_notif_type_2(self):
        ''' Setter method to set the notif type 2 in the database
        this notification will remain until the seller has marked the product sold '''
        #respose data comes from the client side
        pass
    def set_notif_type_3(self):
        pass