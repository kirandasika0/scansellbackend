import redis
from .models import Sale, SaleImage
from users_b.models import User
from django.core import serializers
from search.models import Book
import json
#Creating new redis server
r = redis.Redis(host='pub-redis-18592.us-east-1-2.4.ec2.garantiadata.com',
                port=18592,
                password='kiran@cr7')

#everything releated to feed will be in this file
                
def place_sale(sale, locale):
    locale = locale.split(',').reverse()
    #the locality is from the locale list
    locality = locale[1]
    potential_users = []
    for user in User.objects.all():
        if user.locale.split(',')[1] == locality:
            #this user must see this sale object
            potential_users.append(user)
            
            
            
def generate_feed(user_id):
    user_id = str(user_id)
    user = User.objects.filter(user_id=user_id)[0]
    user_locale_list = user.locale
    user_locale = user.locale.split(',')
    #reversing the list
    user_locale.reverse()
    user_locality = user_locale[1]
    #getting all the sales
    sales = Sale.objects.all()
    feed_products = []
    for sale in sales:
        #check if the locality match and add it to the feed_products list
        sale_locale = sale.location.split(',')
        sale_locale.reverse()
        #getting sale locality
        sale_locality = sale_locale[1]
        
        #checking if the sale location and the user location are the same
        if sale_locality == user_locality:
            #looks like its a match add this object to the array
            feed_products.append(sale)
        
    #we have to serialize the data and return it back
    serialized_data = []
    for sale in feed_products:
        latitude, longitude = sale.geo_point.split(',')
        images = serializers.serialize("json", SaleImage.objects.filter(sale_id=sale.id))
        product_data = {'id': sale.id, 'seller_id': sale.seller_id,
                        'seller_username': sale.seller_username,
                        'book': json.loads(serializers.serialize("json", [sale.book])[1:-1]),
                        'price': sale.price,
                        'location': sale.location,
                        'latitude': latitude,
                        'longitude': longitude,
                        'images': json.loads(images),
                        'extra_info': determine_relation(user_locale_list, sale.location)
                        }
        serialized_data.append(product_data)
    return serialized_data
    
    
def determine_relation(user_locale, sale_locale):
    user_locale = user_locale.split(',')
    sale_locale = sale_locale.split(',')
    matches = 1
    common_grounds = []
    for loc in user_locale:
        if loc in sale_locale:
            matches += 1
            common_grounds.append(loc)
            
    common_grounds = [cg.title() for cg in common_grounds]
    
    if matches >=3:
        relation_string = ','.join(common_grounds)
        relation_string = "Common grounds: " + relation_string
    return relation_string