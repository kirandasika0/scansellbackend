from distance_module.distance_module import *
from .models import Sale

MAX_SEARCH_RADIUS = 1.5

def geo_feed(user, location):
    ''' both user and location are objects '''
    
    # getting all sales objects first
    sales = Sale.objects.all()
    
    #this is the empty list for all sales that are related
    feed_sales = list()
    
    #iterating through all sales
    for sale in sales:
        latitude, longitude = str(sale.geo_point.split(','))
        
        #converting to float
        float(latitude)
        float(longitude)
        
        distance = distance_km(location.latitude, location.longitude,
                                latitude, longitude)
        
        if distance < MAX_SEARCH_RADIUS:
            # given sale is in the range of being bought
            feed_sales.append(sale)
        else:
            continue
        
        return feed_sales
        