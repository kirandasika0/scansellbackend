from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sale, SaleInterest, SaleImage, SaleNotification
from search.models import Book
import json, requests
import redis
from feed import generate_feed, get_relative_feed
from django.core import serializers
from notifications import Notification
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import exceptions
from location import Location
from distance_module.geo_feed import geo_feed
from datetime import datetime
from users_b.models import User
import bmemcached
from utils import MemcacheWrapper
from distance_module.geo_feed_v2 import GeoFeed
from utils import MinPQ
from bid import Bid

# creating a new redis server
r = redis.Redis(host='pub-redis-18592.us-east-1-2.4.ec2.garantiadata.com',
                port=18592,
                password='kiran@cr7')
mc = bmemcached.Client('pub-memcache-17929.us-east-1-2.1.ec2.garantiadata.com:17929',
                        'kiran',
                        'Skd3098309^')
memcache = MemcacheWrapper(mc)

# Create your views here.
def home(request):
    sale = Sale.objects.all()[0]
    sale2 = Sale.objects.all()[1]
    refLocation = Location(32.5903056,-85.5284747)
    print sale.compareTo(sale2, refLocation)
    return HttpResponse("Welcome to the Sale Model App")


#simple title case string view for better type face on app
@csrf_exempt
def title_case_string(request):
    if request.method == 'POST':
        string = request.POST.get('string', "")
        return HttpResponse(json.dumps({'string': string.title()}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")

@csrf_exempt
def new_sale(request):
    if request.method == 'POST':
        seller_id   = request.POST.get('seller_id', "")
        seller_username = request.POST.get('seller_username', "")
        book_id = request.POST.get('book_id', "")
        location = request.POST.get('location', "")
        description = request.POST.get('description', "")
        price = request.POST.get('price', "")
        latitude = request.POST.get('latitude', "")
        longitude = request.POST.get('longitude', "")
        geo_point = latitude + "," + longitude
        if book_id:
            #book is not there please enter the details of the book
            #sending message back to client for uploading contents of book
            #getting the required data
            full_title = request.POST.get('full_title', "")
            link = ""
            uniform_title = request.POST.get('uniform_title', "")
            ean_13 = request.POST.get('barcode_number', "")
            new_book = Book.objects.create(full_title=full_title,
                                            link=link,
                                            uniform_title=uniform_title,
                                            ean_13=ean_13)
            new_book.save()
            #the book is now saved we have to save the sale and enter it in
            #the correct redis bucket for the user
            sale = Sale.objects.create(seller_id=seller_id, seller_username=seller_username,
                                book=new_book, description=description, price=price,
                                location=location, geo_point=geo_point)
            sale.save()
            #we have to create the images
            #front cover image
            front_cover_image = request.POST.get('front_cover_image', "")
            first_cover_image = request.POST.get('first_cover_image', "")
            back_cover_image = request.POST.get('back_cover_image', "")
            #saving all the sale images
            img_names = [front_cover_image, first_cover_image, back_cover_image]
            #img types
            img_types = ['front', 'first', 'back']
            imgs = zip(img_types, img_names)
            for img in imgs:
                SaleImage.objects.create(sale=sale, img_type=img[0],
                                        image_name=img[1])
            # saving this in the memcached for the required users
            memcached_response = {
                'id': sale.id, 'seller_id': sale.seller_id,
                'seller_username': sale.seller_username,
                'description': sale.description,
                'book': json.loads(serializers.serialize("json", [sale.book])[1:-1]),
                'price': sale.price,
                'location': sale.location,
                'latitude': latitude,
                'longitude': longitude,
                'images': json.loads(serializers.serialize("json",SaleImage.objects.filter(sale=sale))),
                'extra_info': sale.location
            }
            # check for which users we have to insert it
            user = User.objects.get(user_id=sale.seller_id)
            user_locale = user.locale.split(',')
            user_locale.reverse()
            user_locality = user_locale[1]
            other_users = User.objects.all()
            for o_user in other_users:
                o_user_locale = o_user.locale.split(',')
                o_user_locale.reverse()
                o_user_locality = o_user_locale[1]

                if user_locality == o_user_locality:
                    # the two locality are equal now we can insert in the memcache
                    memcache.append_data_to_key(sale.seller_id, memcached_response)
            response = {'response': 'Your Sale has been created'}
            return HttpResponse(json.dumps(response),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")



#view for new sale interest
@csrf_exempt
def new_sale_interest(request):
    if request.method == 'POST':
        buyer_id = request.POST.get('buyer_id', "")
        buyer_username = request.POST.get('buyer_username', "")
        sale_id = request.POST.get('sale_id', "")
        if buyer_id and buyer_username and sale_id:
            #get the sale object and then enter it in the database
            sale = Sale.objects.get(pk=sale_id)
            #creating the new sale interest object
            SaleInterest.objects.create(interested_user_id=buyer_id,
                                        interested_username=buyer_username,
                                        sale=sale)
        else:
            return HttpResponse(json.dumps({'reponse': 'Please send the correct data to the server'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send the correct request'}),
                            content_type="application/json")


@csrf_exempt
def new_sale_insert(request):
    if request.method == 'POST':
        return HttpResponse(json.dumps({'response': 0}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send the correct request'}),
                            content_type="application/json")


def redis_test(request):
    return HttpResponse("redis cache")




@csrf_exempt
def create_locale(request):
    ''' This view creates the address for the sale.
        Address format:
        Route, Admininstrative Area Level 3 , Locality, Admininstrative Area Level 2, Admininstrative Level 1,
        State'''
    if request.method == 'POST':
        locale = []
        latitude = request.POST.get('latitude', "")
        longitude = request.POST.get('longitude', "")
        #sending request to google to create locale
        url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude
        try:
            response = json.loads(requests.get(url).content)
        except:
            return_response = "nil"
        #getting the info that we need.
        for obj in response["results"][0]["address_components"]:
            if "route" in obj["types"]:
                locale.append(obj["long_name"])
            if "administrative_area_level_3" in obj["types"]:
                locale.append(obj["long_name"])
            if "locality" in obj["types"]:
                locale.append(obj["long_name"])
            if "administrative_area_level_2" in obj["types"]:
                locale.append(obj["long_name"])
            if "administrative_area_level_1" in obj["types"]:
                locale.append(obj["short_name"])
        return_response = ','.join(locale).upper()
        return HttpResponse(json.dumps({'response': return_response}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")


@csrf_exempt
def get_feed(request):
    if request.method == 'GET':
        #get all the posts from the data base
        user_id = request.GET.get('user_id', "")
        if user_id:
            try:
                user_notifications = len(SaleNotification.objects.filter(user_id=user_id))
            except (SaleNotification.DoesNotExist) as e:
                user_notifications = 0
            data = []
            #check if there in memcache
            data = generate_feed(user_id)
            # try:
            #     data = generate_feed(user_id)
            # except (exceptions.UserForIDNotFoundException) as e:
            #     data.append({'error': str(e)})
            response = {'response': data,
                        'current_app_version': '1.0',
                        'user_notifications_number': user_notifications}
            return HttpResponse(json.dumps(response, indent=4), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'response': 'please provide a user_id'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send the correct request'}),
                            content_type="application/json")


@csrf_exempt
def sale_notification(request):
    if request.method == 'POST':
        #get the notif data
        data = {'notif_type': request.POST.get('notif_type', ""),
                'seller_id': request.POST.get('seller_id', ""),
                'seller_username': request.POST.get('seller_username', ""),
                'sale_id': request.POST.get('sale_id', ""),
                'buyer_id': request.POST.get('buyer_id', ""),
                'buyer_username': request.POST.get('buyer_username', "")}
        if data['notif_type'] == "1":
            notif = Notification(1, data)
            return HttpResponse(json.dumps(notif.set_notif_type_1()), content_type="application/json")
        if data['notif_type'] == "2":
            notif = Notification(2, data)
            return HttpResponse(json.dumps(notif.set_notif_type_2(request.POST.get('notif_1_id', ""))), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")

@csrf_exempt
def get_notifications(request):
    user_id = request.GET.get('user_id', "")
    if user_id:
        notifications = SaleNotification.objects.filter(user_id=user_id)
        notifs_list = []
        for notification in notifications:
            response_dict = {'notif_type': notification.notif_type,
                            'id': notification.id,
                            'user_id': notification.user_id,
                            'username': notification.user_name,
                            'data': json.loads(notification.data),
                            'sale_id': notification.sale_id}
            notifs_list.append(response_dict)
        return HttpResponse(json.dumps({'response': notifs_list}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'user_id not found'}),
                            content_type="application/json")

@csrf_exempt
def delete_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id', "")
        if notification_id:
            # delete the given notification
            if SaleNotification.objects.get(pk=int(notification_id)).delete():
                return HttpResponse(json.dumps({'response': 'true del'}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'response': 'error in deleting'}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'response': 'please send notification id'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")
@csrf_exempt
def test_patch(request):
    if request.method == 'PATCH':
        return HttpResponse('Welcome this is a patch request')
    else:
        return HttpResponse('Fuck you')



@csrf_exempt
def geo_feed_view(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        latitude = float(request.GET.get('lat'))
        longitude = float(request.GET.get('long'))

        if user_id and latitude and longitude:
            current_time = datetime.now()
            user_location = Location(latitude, longitude, current_time)
            user = User.objects.get(user_id=user_id)

            feed_results = geo_feed(user, user_location)

            return HttpResponse(json.dumps(feed_results),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'repsonse': 'please send requied data'}),
                                content_type="application/json")

@csrf_exempt
def geo_feedv2(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        latitude = float(request.GET.get('lat'))
        longitude = float(request.GET.get('long'))

        if user_id and latitude and longitude:
            current_time = datetime.now()
            user_location = Location(latitude, longitude, current_time)
            user = User.objects.get(user_id=user_id)

            geo_feed = GeoFeed(user, location)


            return HttpResponse(json.dumps(geo_feed.serialize_sales()),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'repsonse': 'please send requied data'}),
                                content_type="application/json")

@csrf_exempt
def sliderFeed(request):
    pass


@csrf_exempt
def hotDeals(request):
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        dealsKey = userId + "_hotDeals"
        pq = MinPQ()
        pq.deserialize(dealsKey, memcache)
        if pq.size == 0:
            # make a new queue and save it
            sales = Sale.objects.all()
            for sale in sales:
                pq.enqueue(sale)
            minSale = pq.dequeue()
            pq.serialize(dealsKey, memcache)
            return HttpResponse(serializers.serialize("json", [minSale])[1:-1],
                                content_type="application/json")
        else:
            minSale = pq.dequeue()
            pq.serialize(dealsKey, memcache)
            return HttpResponse(serializers.serialize("json", [minSale])[1:-1],
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Only POST requests are allowed.'}),
                            content_type="application/json")


# Helper methods
@csrf_exempt
def getSaleImages(request):
    if request.method == 'POST':
        saleId = request.POST.get('sale_id')
        sale = Sale.objects.get(pk=int(saleId))
        saleImages = SaleImage.objects.filter(sale=sale)
        if saleImages:
            return HttpResponse(serializers.serialize("json", saleImages),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error': 'An unknown error occured'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Please send a POST request'}),
                            content_type="application/json")

@csrf_exempt
def markSold(request):
    if request.method == 'POST':
        saleId = request.POST.get('sale_id')
        sale = Sale.objects.get(pk=saleId)
        # marking given sale as sold
        sale.sold = True
        sale.save()
        return HttpResponse(json.dumps({'response': True}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Only POST requests.'}),
                            content_type="application/json")
# END HELPER METHODS


@csrf_exempt
def placeBid(request):
    if request.method == 'POST':
        saleId = request.POST.get('sale_id')
        userId = request.POST.get('user_id')
        bidPrice = request.POST.get('bid_price')
        user = User.objects.get(user_id=userId)
        bidCacheKey = saleId + "_bid"
        if memcache.get_val(bidCacheKey) == False:
            # This is the first bid on the sale
            sale = Sale.objects.get(pk=saleId)
            # Creating a new bid from Bid Class
            bid = Bid(sale)
            bid.place_bid(user, bidPrice=bidPrice)
            if bid.serialize(memcache):
                return HttpResponse(json.dumps({'response': True}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error': 'error bidding.'}),
                                    content_type="application/json")
        else:
            # Bid is already there now deserialize it.
            bid = Bid()
            bid.deserialize(bidCacheKey, memcache)
            bid.place_bid(user, bidPrice=bidPrice)
            if bid.serialize(memcache):
                return HttpResponse(json.dumps({'response': True}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error': 'error bidding.'}),
                                    content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send POST request.'}),
                            content_type="application/json")

@csrf_exempt
def bidStats(request):
    if request.method == 'POST':
        saleId = request.POST.get('sale_id')
        bidCacheKey = saleId + "_bid"
        if memcache.get_val(bidCacheKey) is not False:
            bid = Bid()
            bid.deserialize(bidCacheKey, memcache)
            return HttpResponse(json.dumps(bid.stats()),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error': 'error getting stats'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'send POST request.'}),
                            content_type="application/json")
