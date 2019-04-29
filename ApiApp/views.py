from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist

from .modelSerializers import RoomsSerializer, DeviceSerializer,RemoteDevicePanelSerializer
from RemoteApp.models import Rooms,Devices,Command


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


class DeviceView(APIView):

    parser_classes = (JSONParser,)
    def get(self, request,id):
        response = Response()
        device=None
        command=None
        try:
            device=Devices.objects.get(id=id)

            command=Command.objects.filter(device=device)
        except ObjectDoesNotExist:


            response.status_code = 400
            response.data = "Device doesn't exist"
            return response

        devSerilizer = RemoteDevicePanelSerializer(command,many=True)

        response = Response(devSerilizer.data)
        response["Access-Control-Allow-Origin"] = "*"

        return response


    def put(self,request,id):
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        device = None
        command = None
        try:

            device = Devices.objects.get(id=id)

            commandId=request.data["command"]
            value=int(request.data["value"])
            commands = Command.objects.filter(device=device)
            command=commands.get(id=commandId)
            if(not id==command.device.id):

                response.status_code=400
                response.data="device has no such command"
                return response

            commandSucces=command.setValue(value)

            if(commandSucces):
                response.status_code=202
                response.data="Success"
            else:
                response.status_code=412
                response.data="Value is not valid"

            return response

        except ObjectDoesNotExist:

            response.status_code = 400
            response.data = "Device doesn't exist"
            return response
        except ValueError:
            response.status_code=400
            response.data="Value mast be is int"
            return response



class DevicesView(APIView):
    parser_classes = (JSONParser,)
    def get(self, request):
        devices=Devices.objects.all()
        devSerilizer=DeviceSerializer(devices, many=True)

        response=Response(devSerilizer.data)
        response["Access-Control-Allow-Origin"] = "*"
        return response


    def post(self, request):


        response=Response()
        response["Access-Control-Allow-Origin"] = "*"

        try:
            device=Devices()
            device.name=request.data["name"]
            device.driverPath=request.data["driverPath"]
            device.iconPath=request.data["icon"]
            roomId=int(request.data["roomId"])
            device.template=request.data["template"]
            device.room=Rooms.objects.get(id=roomId)
            device.save()
            response.data="device created"
            return response
        except ValueError:
            response.status_code=400
            response.data="roomId is not integer"
            return response
        except KeyError:
            response.status_code=400
            response.data="Incomplete data"
            return response

