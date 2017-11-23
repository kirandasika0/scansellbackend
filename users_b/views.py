import json
import bmemcached
from datetime import datetime

from django.http import QueryDict
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from sale.models import Sale
from sale.utils import MemcacheWrapper
from scansell.utils import ServeResponse

from .models import User
from .forms import UserSignupForm
from .utils import id_generator, create_locale, password_generator, sort_usernames, contains_user

# Creating an instance of Memcache here
mc = bmemcached.Client('pub-memcache-10484.us-east-1-1.2.ec2.garantiadata.com:10484',
                        'saikiran',
                        'Skd30983')
memcache = MemcacheWrapper(mc)

# Create your views here.
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

@csrf_exempt
def allUsers(request):
    users = User.objects.all()
    return HttpResponse(serializers.serialize("json", users),
                        content_type="application/json")



######################## CLASS BASED VIEWS START HERE ######################

class SignupView(View):
    """ Main SignupView for user signups and validations. """
    
    def get(self, request):
        return ServeResponse.serve_error("GET request forbidden.", 403)
    
    def post(self, request):
        user_id = id_generator()
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number', "")
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        try:
            locale = create_locale(latitude, longitude)
        except ValueError:
            locale = ""
        password = password_generator(request.POST.get('password'))
        redis_key = user_id + "_feed"
        
        if len(User.objects.filter(username=username)) == 0:
            user = User.objects.create(user_id=user_id, username=username,
                                        password=password,
                                        email=email, mobile_number=mobile_number,
                                        locale=locale, redis_key=redis_key)
            if user is not None:
                return ServeResponse.serve_response(serializers.serialize("json", [user])[1:-1], 201)
            else:
                return ServeResponse.serve_error("error while create user.", 403)
        else:
            return ServeResponse.serve_error("user already exists", 403)

        return ServeResponse.serve_response({'response': True}, 200)


class LoginView(View):
    """ Main login view for all users. """

    def get(self, reqeust):
        return ServeResponse.serve_error("GET request not allowed.", 403)

    def post(self, request):
        username = request.POST.get('username')
        password = password_generator(request.POST.get('password'))

        if len(username) < 1 or len(password) < 1:
            return ServeResponse.serve_error("username or password not provided", 403)

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return ServeResponse.serve_error("incorrect username or password", 403)
        if user.password == password:
            return ServeResponse.serve_response(serializers.serialize("json", [user])[1:-1], 200)

        return ServeResponse.serve_error("incorrect username or password", 403)


class UpdateLocationView(View):
    """ Updates the user location everytime user opens the app. """

    def get(self, request):
        return ServeResponse.serve_error("GET not allowed.", 500)

    def post(self, request):
        user_id = request.POST.get('user_id')
        memcache_key = request.POST.get('memcache_key')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if memcache.get_val(memcache_key):
            memcache.append_data_to_key(memcache_key, (latitude, longitude, created_at))
        else:
            memcache.set_key_value(memcache_key, (latitude, longitude, created_at))
        
        return ServeResponse.serve_response({"status": 200, "info": "updated"}, 200)
