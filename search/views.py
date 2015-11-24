from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from insert_books import *
import json
# Create your views here.
def home(reqeust):
    return HttpResponse("Welcome", content_type="application/json")
    

@csrf_exempt
def test_view(reqeust):
    if request.method == 'POST':
        name = request.POST.get('name', "")
        return HttpResponse(json.dumps({'response': name}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send the correct request'}), 
                            content_type="application/json")
