from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User

# Create your views here.
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
            return HttpResponse(json.dumps({'response': 'user has been created'}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'response': 'there was a problem in creating the user'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}), 
                            content_type="application/json")