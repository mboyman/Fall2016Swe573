from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello Michael BOYMAN. You are at the polls index()")
