from django.shortcuts import render


def index(request):

    HomeParameters=dict()

    HomeParameters["temperature"]=22
    HomeParameters["humidity"]=60
    HomeParameters["presure"]=761
    HomeParameters["Controls"]=tuple(range(30))

    return render(request,"RemoteApp/main.html", context=HomeParameters)
# Create your views here.

