from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

def home(request):
    return HttpResponse("Welcome", content_type="application/json")
    
    
@csrf_exempt
def test(request):
    if request.method == 'POST':
        name = request.POST.get('name', "")
        return HttpResponse(json.dumps({'response': name}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'Please send the correct request'}),
                            content_type="application/json")
                            