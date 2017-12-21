from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    """ Main index route """
    return render(request, "index.html", {})