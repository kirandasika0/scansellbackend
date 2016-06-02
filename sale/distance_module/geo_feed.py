from distance_module import distance_km
from sale.models import Sale, SaleImage
from django.core import serializers
import json

MAX_SEARCH_RADIUS = 2.5

def geo_feed(user, location):
    ''' both user and location are objects '''
    
    # getting all sales objects first
    sales = Sale.objects.all()
    
    #this is the empty list for all sales that are related
    feed_sales = list()
    
    #iterating through all sales
    for sale in sales:
        latitude, longitude = sale.geo_point.split(',')
        
        latitude = float(latitude)
        longitude = float(longitude)
        
        distance = distance_km(location.latitude, location.longitude, latitude, longitude)
        
        if distance < MAX_SEARCH_RADIUS:
            # given sale is in the range of being bought
            feed_sales.append(sale)
        else:
            continue
        
    response_list = list()
    
    for sale in feed_sales:
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
        