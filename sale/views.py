from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sale, SaleInterest, SaleImage
from search.models import Book
import json, requests
import redis
# creating a new redis server
r = redis.Redis(host='pub-redis-18592.us-east-1-2.4.ec2.garantiadata.com',
                port=18592,
                password='kiran@cr7')
# Create your views here.
def home(request):
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
def sale_notification(request):
    """ All main sale notification will be sent from this view """
    return HttpResponse(json.dumps({'response': 'send the appropriate request'}),
                        content_type="application/json")
                        
                        

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
        response = json.loads(requests.get(url).content)
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
        sales = Sale.objects.all()
        return HttpResponse(sales, content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send the correct request'}),
                            content_type="application/json")