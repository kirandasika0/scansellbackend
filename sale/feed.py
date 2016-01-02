import redis
from .models import Sale
from users_b.models import User
from django.core import serializers
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
    user = User.objects.get(user_id=user_id)
    user_redis_key = user.redis_key
    user_locale = user.locale.split(',')
    #reversing the list
    user_locale.reverse()
    user_locality = user_locale[1]
    #getting all the sales
    sales = Sales.objects.all()
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
    for book in feed_products:
        latitude, longitude = book.geo_point.split(',')
        product_data = {'id': book.id, 'seller_id': book.seller_id,
                        'seller_username': book.seller_username,
                        'book': serializers.serialize("json", [obj])[1:-1],
                        'price': book.price,
                        'location': book.location,
                        'latitude': latitude,
                        'longitude': longitude,
                        'pub_date': book.created_at}
        serialized_data.append(product_data)
    return serialized_data