from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Scan&Sell backend.", content_type="application/json")