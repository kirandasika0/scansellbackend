from django.http import HttpResponse

def index(request):
    if len(request.META) > 0:
        try:
            print request.META['HTTP_AUTHORIZATION']
            return HttpResponse("quicksell api", content_type="application/json", status=200)
        except KeyError:
            return HttpResponse("quicksell api", content_type="application/json", status=403)