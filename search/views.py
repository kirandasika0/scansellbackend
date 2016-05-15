from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Book

def home(request):
    return HttpResponse("Welcome", content_type="application/json")
    
    
@csrf_exempt
def insert_book(request):
    if request.method == 'POST':
        full_title = request.POST.get('full_title', "")
        link = request.POST.get('link', "")
        uniform_title = request.POST.get('uniform_title', "")
        if len(full_title) > 0 and len(link) > 0 and len(uniform_title) > 0:
            try:
                #insert the book into the database
                Book.objects.create(full_title=full_title, link=link, uniform_title=uniform_title)
                return HttpResponse(json.dumps({'response': 'inserted'}), content_type="application/json")
            except:
                print "shit"
                return HttpResponse(json.dumps({'response': 'looks like there was a problem entering it'}), 
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'response': 'looks like there is no data'}),
                                content_type="application/json")
                                
    else:
        return HttpResponse(json.dumps({'response': 'send correct request'}),
                            content_type="application/json")
                            
                            
@csrf_exempt
def new_search(request):
    if request.method == 'POST':
        search_string = request.POST.get('search_string', "")
        return HttpResponse(json.dumps({'response': search_string}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")
                            
@csrf_exempt
def search_book(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_string')
        return HttpResponse(search_query)
    else:
        return HttpResponse('fd')