from distance_module import distance_km
from sale.models import Sale, SaleImage
from django.core import serializers
from users_b.models import User
from location import Location
import json

SEARCH_RADIUS = 2.5

class GeoFeed(object):
    def __init__(self, user, location):
        self.user = user
        self.location = location
        self.sales = list()
        
    def getUser(self):
        return self.user
        
    def getLocation(self):
        return self.location
    
    def setSales(self):
        pass
    
    def getNearbySales(self):
        # get the sales nearby
        sales = Sale.objects.all()
        for sale in sales:
            saleLatitude, saleLongitude = sale.geo_point.split(',')
            saleLatitude = float(saleLatitude)
            saleLongitude = float(saleLongitude)
            
            
            distance = distance_km(self.location.latitude, self.location.longitude,
                                    saleLatitude, saleLongitude)
            
            if distance <= SEARCH_RADIUS:
                yield sale
        
    def serialize_sales(self, sales):
        response_list = list()
        for sale in self.getNearbySales():
            response = {
                'pk': sale.pk,
                'model': 'sale.sale',
                'fields': {
                    'description': sale.description,
                    'seller_id': sale.seller_id,
                    'seller_username': sale.seller_username,
                    'price': sale.price,
                    'location': sale.location,
                    'geo_point': sale.geo_point,
                    'book': json.loads(serializers.serialize("json", [sale.book])[1:-1]),
                    'images': json.loads(serializers.serialize("json", SaleImage.objects.filter(sale=sale))),
                    'created_at': sale.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
        }
        response_list.append(response)
        return response_list