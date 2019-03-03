from rest_framework.views import APIView
from rest_framework.response import Response


class api(APIView):

    def get(self,request):
        return Response("aaa")

# Create your views here.


