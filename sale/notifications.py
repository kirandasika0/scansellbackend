import json
import time
from .models import SaleNotification, Sale
from search.models import Book
from django.core import serializers
from users_b.models import User
###########################################
# All imports above this comment
'''
Defining all the notification types

Notification Type 1 - Request to the seller from a random buyer/user
    *This type of notification only comes once per product and per buyer
    *If the seller accepts this request then his information is passed to the 
    buyer
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
    # Constructer method to take input the
    def __init__(self, notif_type, data):
        self.notif_type = notif_type
        self.data = data
    
    def __str__(self):
        return "Notification Type: " + self.notif_type
    
    def set_notif_type_1(self):
        ''' Setter method to set the notif 1 type in the database
        make sure the type and the data go in correct '''
        # the data that has come form client side
        response = self.data
        notif_for_sale = Sale.objects.get(pk=int(response["sale_id"]))
        notif_string = response["buyer_username"] + " is interested in your book " + notif_for_sale.book.uniform_title.upper() + "."
        notif_data = json.dumps({'notif_type': 1, 'buyer_id': response["buyer_id"],
                    'buyer_username': response["buyer_username"],
                    'buyer_username': response["buyer_username"],
                    'notification_string': notif_string})
                                        
        # check if the notification is there by the same user
        notifs = SaleNotification.objects.filter(notif_type=1, user_id=response["seller_id"], sale_id=response["sale_id"])
        if len(notifs) == 0:
            SaleNotification.objects.create(notif_type=1, user_id=response["seller_id"],
                                                user_name = response["seller_username"],
                                                sale = Sale.objects.get(pk=int(response["sale_id"])),
                                                data=notif_data)
        for notif in notifs:
            if response["buyer_id"] not in json.loads(notif.data).values():
               # inserting data into the database
               SaleNotification.objects.create(notif_type=1, user_id=response["seller_id"],
                                                user_name = response["seller_username"],
                                                sale = Sale.objects.get(pk=int(response["sale_id"])),
                                                data=notif_data) 
        return {'response': 'true'}
        
    def set_notif_type_2(self, notif_type_1_id):
        ''' Setter method to set the notif type 2 in the database
        this notification will remain until the seller has marked the product sold '''
        # respose data comes from the client side
        response = self.data
        # getting the user
        buyer_user_json = json.loads(serializers.serialize('json', [User.objects.get(user_id=response["seller_id"])])[1:-1])
        seller_user_json = json.loads(serializers.serialize('json', [User.objects.get(user_id=response["buyer_id"])])[1:-1])
        current_sale = Sale.objects.get(pk=int(response["sale_id"]))
        #notification string for the buyer in the app
        notification_string_buyer = "You can now contact " + response["seller_username"] + " regarding " + current_sale.book.uniform_title.upper() + " purchase."
        #notification string for the seller in the app
        notification_string_seller = "You can now contact " + response["buyer_username"] + " regarding " + current_sale.book.uniform_title.upper() + " sale."
        
        notif_data_buyer = {'notif_type': 2, 'user_data': buyer_user_json, 'notification_string': notification_string_buyer}
        notif_data_seller = {'notif_type': 2, 'user_data': seller_user_json, 'notification_string': notification_string_seller}
        
        buyer_notification = SaleNotification.objects.create(notif_type=2, user_id=response["buyer_id"],
                                                            user_name=response["buyer_username"],
                                                            sale=current_sale,
                                                            data=json.dumps(notif_data_buyer))
        buyer_notification.save()
        
        seller_notification = SaleNotification.objects.create(notif_type=2, user_id=response["seller_id"],
                                                            user_name=response["seller_username"],
                                                            sale=current_sale,
                                                            data=json.dumps(notif_data_seller))
        seller_notification.save()
        
        # deleting the notif type 1 notifiction
        notif_to_del = SaleNotification.objects.get(pk=int(notif_type_1_id)).delete()
        
        return {'response': 'true'}
        
    def set_notif_type_3(self):
        pass
    