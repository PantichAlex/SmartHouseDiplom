from django.shortcuts import render

from .RemoteModel.HomeStatistics import HomeStatistics

def index(request):

    HomeParameters=dict()

    HomeParameters["statistic"]=HomeStatistics()

    HomeParameters["Controls"]=tuple(range(30))

    return render(request,"RemoteApp/main.html", context=HomeParameters)
# Create your views here.

