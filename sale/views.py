from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sale
from search.models import Book
import json
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
        seller_id = request.POST.get('seller_id', "")
        seller_username = request.POST.get('seller_username', "")
        book_id = request.POST.get('book_id', "")
        description = request.POST.get('description', "")
        price = request.POST.get('price', "")
    else:
        return HttpResponse(json.dumps({'response': 'please send the correct request'}),
                            content_type="application/json")