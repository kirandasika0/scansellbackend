from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt
import bmemcached
from sale.utils import MemcacheWrapper
from datetime import datetime
from utils import id_generator, create_locale, password_generator
from django.core import serializers
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
        latitude = request.POST.get('latitude', "")
        longitude = request.POST.get('longitude', "")
        locale = create_locale(latitude, longitude)
        password = password_generator(request.POST.get('password', ""))
        redis_key = user_id + "_feed"
        
        # Save the user
        user = User.objects.create(user_id=user_id, username=username,
                                    password=password,
                                    email=email, mobile_number=mobile_number,
                                    locale=locale, redis_key=redis_key)
        user.save()
        
        return HttpResponse(serializers.serialize("json", [user])[1:-1],
                            content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({'response': 'view only allows POST reqeusts.'}),
                            content_type="application/json")

@csrf_exempt
def login(request):
    pass
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