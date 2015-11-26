from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sale, SaleInterest
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
        seller_id   = request.POST.get('seller_id', "")
        seller_username = request.POST.get('seller_username', "")
        book_id = request.POST.get('book_id', "")
        description = request.POST.get('description', "")
        price = request.POST.get('price', "")
        if book_id != 0:
            if Book.objects.get(pk=book_id).exists():
                #the book that the user wants to sell is available
                book = Book.objects.get(pk=book_id)
                #creating a new sale for the book that the user has chosen
                Sale.objects.create(seller_id=seller_id, seller_username=seller_username,
                                    book=book, description=description, price=price)
            else:
                #book is not there please enter the details of the book
                #sending message back to client for uploading contents of book
                response = {'response': 3}
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