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

        response=Response(roomSerializer.data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class Register(APIView):

    def get(self, request):

        print(request.GET)
        return Response("aaa")

    def post(self, request):
        pass


class Login(APIView):

    def post(self, request):
        return Response("Login")


class GetDeviceView(APIView):

    def get(self, request,id):

        device=Devices.objects.get(id=id)
        devSerilizer = DeviceSerializer(device)

        response = Response(devSerilizer.data)
        response["Access-Control-Allow-Origin"] = "*"

        return response

class DevicesView(APIView):

    def get(self, request):
        devices=Devices.objects.all()
        devSerilizer=DeviceSerializer(devices, many=True)

        response=Response(devSerilizer.data)
        response["Access-Control-Allow-Origin"] = "*"
        return response


