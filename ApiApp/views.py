from rest_framework.views import APIView
from rest_framework.response import Response



from .modelSerializers import RoomsSerializer, DeviceSerializer
from RemoteApp.models import Rooms,Devices


class Api(APIView):

    def get(self,request):
        return Response("aaa")


class RoomsView(APIView):

    def get(self,request):
        rooms=Rooms.objects.all()
        roomSerializer=RoomsSerializer(rooms, many=True)

        return Response(roomSerializer.data)

class Register(APIView):

    def get(self, request):

        print(request.GET)
        return Response("aaa")


class DevicesView(APIView):

    def get(self, request):
        devices=Devices.objects.all()
        devSerilizer=DeviceSerializer(devices, many=True)

        resp=Response(devSerilizer.data)
        resp["Access-Control-Allow-Origin"] = "*"
        return resp


