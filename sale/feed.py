import json
import redis
import Feed_pb2

from google.protobuf import json_format

from django.core import serializers

from users_b.models import User
from search.models import Book
from sale.exceptions import UserForIDNotFoundException

from .models import Sale, SaleImage

# Creating new redis server
r = redis.Redis(host='pub-redis-18592.us-east-1-2.4.ec2.garantiadata.com',
                port=18592,
                password='kiran@cr7')

# everything releated to feed will be in this file


def place_sale(sale, locale):
    locale = locale.split(',').reverse()
    # the locality is from the locale list
    locality = locale[1]
    potential_users = []
    for user in User.objects.all():
        if user.locale.split(',')[1] == locality:
            # this user must see this sale object
            potential_users.append(user)


def generate_feed(user_id):
    user_id = str(user_id)
    user_redis_key = user_id + "_feed"

    # Raise exception if user not found in database
    try:
        user = User.objects.get(user_id=user_id)
    except (User.DoesNotExist):
        raise UserForIDNotFoundException("user with id " + user_id + " not found.")
    
    user_locale_list = user.locale
    user_locale = user.locale.split(',')
    # reversing the list
    user_locale.reverse()
    user_locality = user_locale[1]
    # getting all the sales
    sales = Sale.objects.filter(sold=False)
    feed_products = []
    for sale in sales:
        # check if the locality match and add it to the feed_products list
        sale_locale = sale.location.split(',')
        sale_locale.reverse()
        # getting sale locality
        sale_locality = sale_locale[1]

        # checking if the sale location and the user location are the same
        if sale_locality == user_locality:
            # looks like its a match add this object to the array
            feed_products.append(sale)

    # we have to serialize the data and return it back
    serialized_data = []
    for sale in feed_products:
        latitude, longitude = sale.geo_point.split(',')
        images = serializers.serialize("json",
                        SaleImage.objects.filter(sale_id=sale.id))
        product_data = {'id': sale.id, 'seller_id': sale.seller_id,
                        'seller_username': sale.seller_username,
                        'description': sale.description,
                        'book': json.loads(serializers.serialize("json", [sale.book])[1:-1]),
                        'price': sale.price,
                        'location': sale.location,
                        'latitude': latitude,
                        'longitude': longitude,
                        'images': json.loads(images),
                        'extra_info': determine_relation(user_locale_list, sale.location),
                        'sold': sale.sold
                        }
        serialized_data.append(product_data)
    return serialized_data

# we might want to rerank all the results based on the number of matches
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
        # filtering matches
        # removing the state first
        common_grounds.pop(len(common_grounds) - 1)
        # removing the county
        common_grounds.pop(len(common_grounds) - 1)
        relation_string = ', '.join(common_grounds)
    else:
        relation_string = ', '.join(common_grounds)
    return relation_string

def sale_relationship(user_locale, sale_locale):
    # creating a common ground list
    common_grounds = []
    user_locale = user_locale.split(',')
    sale_locale = sale_locale.split(',')
    matches = 0
    for loc in user_locale:
        if loc in sale_locale:
            matches += 1
            common_grounds.append(loc)

    # title casing the common ground list
    common_grounds = [loc.title() for loc in common_grounds]
    return_dict = {}
    if matches >=3:
        common_grounds.pop(len(common_grounds)-1)
        return_dict = {'common_grounds': ', '.join(common_grounds),
                        'matches': matches}
    else:
        return_dict = {'common_ground': ', '.join(common_grounds),
                        'matches': matches}
    return return_dict

def get_relative_feed(user_id):
    # get the redis key of the user
    user_id = str(user_id)
    user = User.objects.get(user_id=user_id)
    # user redis key
    user_redis_key = user.redis_key

    hasRedisKey = (False, True)[r.exists(user_redis_key) == True]
    # now check if the redis key is available
    if hasRedisKey == True:
        print(r.get(user_redis_key))
        return json.loads(r.get(user_redis_key))['user_feed']
    else:
        # now saving the feed in the redis box
        new_user_feed = {'user_feed': generate_feed(user_id)}
        r.set(user_redis_key, new_user_feed)
        return new_user_feed['user_feed']


def create_geofence(user_id="ME6lnbVxR9"):
    ''' this function will create a geofence for a user based on his location '''
    pass



##################### NEW FEED ALGORITHM ########################
class GeoFeed(object):
    """ Class to represent the feed of books shown in the app. """

    def __init__(self, user=None):
        if user is None:
            raise AttributeError("user is needed")
        self.user = user
        self.set_address()
        # Long list of sales in the database
        self.sales = list(Sale.objects.filter(sold = False))

    def __iter__(self):
        return self

    def next(self):
        """ Gives the next product in iterator. """
        try:
            current_sale = self.sales.pop()
        except IndexError:
            raise StopIteration
        
        sale_locality = self.get_address_list(current_sale.location)[-2]

        if self.user_locality == sale_locality:
            return current_sale

        # Returning None if sale does not belong to user locality
        return None
    
    def set_address(self):
        self.user_address_list = self.get_address_list(self.user.locale)
        self.user_locality = self.user_address_list[-2]

    def get_address_list(self, address):
        """ Get the address in a list form. """
        return address.split(',')

    def serialize_proto(self, is_json=False):
        """ Use protobuf to serialize to bytes as its faster. """
        feed = Feed_pb2.Feed()
        for temp_sale in self:
            # Continue iteration if None occurs
            if temp_sale is None:
                continue
            # Add sale object to feed protobuf
            sale = Feed_pb2.Sale()
            sale.id = temp_sale.pk
            sale.seller_id = temp_sale.seller_id
            sale.seller_username = temp_sale.seller_username
            # Sale book
            temp_sale_book = temp_sale.book
            sale.book.id = temp_sale_book.pk
            sale.book.full_title = temp_sale_book.full_title
            sale.book.link = temp_sale.book.link
            sale.book.uniform_title = temp_sale_book.uniform_title
            sale.book.ean13 = temp_sale_book.ean_13

            # Sale Images
            sale_images = SaleImage.objects.filter(sale=temp_sale)
            for image in sale_images:
                sale_image = Feed_pb2.SaleImage()
                sale_image.sale_id.MergeFrom(sale)
                sale_image.img_type = image.img_type
                sale_image.image_name = image.image_name

                # Append to sale.images
                sale.images.extend([sale_image])

            feed.sales.extend([sale])

        if is_json:
            return json_format.MessageToJson(feed)
        return feed.SerializeToString()
    
    def serialize(self):
        serialized_data = []
        for sale in self:
            if sale is None:
                continue
            latitude, longitude = sale.geo_point.split(',')
            images = serializers.serialize("json",
                            SaleImage.objects.filter(sale_id=sale.id))
            product_data = {'id': sale.id, 'seller_id': sale.seller_id,
                            'seller_username': sale.seller_username,
                            'description': sale.description,
                            'book': json.loads(serializers.serialize("json", [sale.book])[1:-1]),
                            'price': sale.price,
                            'location': sale.location,
                            'latitude': latitude,
                            'longitude': longitude,
                            'images': json.loads(images),
                            'extra_info': determine_relation(self.user.locale, sale.location),
                            'sold': sale.sold
                            }
            serialized_data.append(product_data)
        return serialized_data
