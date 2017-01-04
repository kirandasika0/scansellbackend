from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt
import bmemcached
from sale.utils import MemcacheWrapper
from sale.models import Sale
from datetime import datetime
from utils import id_generator, create_locale, password_generator
from django.core import serializers
from utils import sort_usernames, contains_user
#creating an instance of Memcache here
mc = bmemcached.Client('pub-memcache-10484.us-east-1-1.2.ec2.garantiadata.com:10484',
                        'saikiran',
                        'Skd30983')
memcache = MemcacheWrapper(mc)
# Create your views here.
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', "")
        username = request.POST.get('username', "")
        email = request.POST.get('email', "")
        mobile_number = request.POST.get('mobile_number', "")
        locale = request.POST.get('locale', "")
        redis_key = request.POST.get('redis_key', "")
        if user_id and username and email and mobile_number and locale and redis_key:
            #make the user
            user = User.objects.create(user_id=user_id, username=username,
                                        email=email, mobile_number=mobile_number,
                                        locale=locale, redis_key=redis_key)
            user.save()
            return HttpResponse(json.dumps({'response': 'true'}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'response': 'there was a problem in creating the user'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")


@csrf_exempt
def signUpUser(request):
    if request.method == 'POST':
        user_id = id_generator()
        username = request.POST.get('username', "")
        email = request.POST.get('email', "")
        mobile_number = request.POST.get('mobile_number', "")
        latitude = request.POST.get('latitude')
        print "\n\n"
        print latitude
        longitude = request.POST.get('longitude')
        print longitude
        print "\n\n"
        locale = create_locale(latitude, longitude)
        password = password_generator(request.POST.get('password', ""))
        redis_key = user_id + "_feed"

        print "\n\n"
        print (username, password)
        print "\n\n"

        # check if the user is already present
        sorted_users = sort_usernames(User.objects.all())

        if not contains_user(username, sorted_users):
             # Save the user
            user = User.objects.create(user_id=user_id, username=username,
                                        password=password,
                                        email=email, mobile_number=mobile_number,
                                        locale=locale, redis_key=redis_key)
            user.save()

            return HttpResponse(serializers.serialize("json", [user])[1:-1],
                                content_type="application/json")
        else:
            response = {'error': 'user with that username already exists. please try something else.'}
            return HttpResponse(json.dumps(response),
                                content_type="application/json")

    else:
        return HttpResponse(json.dumps({'response': 'view only allows POST reqeusts.'}),
                            content_type="application/json")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = password_generator(request.POST.get('password'))
        if username and password:
            #fetching the user object form database
            try:
                user = User.objects.get(username=username)
            except:
                return HttpResponse(json.dumps({'error': 'username or password incorrect'}),
                                    content_type="application/json")

            if password == user.password:
                return HttpResponse(serializers.serialize("json", [user])[1:-1],
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error':'username or password incorrect'}),
                                    content_type="application/json")

    else:
        return HttpResponse(json.dumps({'response': 'only POST requests allowed'}),
                            content_type="application/json")
@csrf_exempt
def update_location(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        memcache_key = request.POST.get('memcache_key')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if memcache.get_val(memcache_key):
            memcache.append_data_to_key(memcache_key, (latitude, longitude, created_at))
            return HttpResponse(json.dumps({'response': 'done'}), content_type="application/json")
        else:
            memcache.set_key_value(memcache_key, (latitude, longitude, created_at))
            return HttpResponse(json.dumps({'response': 'done'}), content_type="appliaction/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send data.'}),
                            content_type="application/json")


@csrf_exempt
def mySales(request):
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        sales = Sale.objects.filter(seller_id=userId)
        return HttpResponse(serializers.serialize("json", sales),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Only POST requests.'}),
                            content_type="application/json")
