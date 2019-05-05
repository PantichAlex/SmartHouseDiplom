#-*-coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from hashlib import md5
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from validate_email import validate_email

from .apiDecorators import auth
from .modelSerializers import RoomsSerializer, DeviceSerializer,RemoteDevicePanelSerializer
from .Permissions import AuthPermissions
from RemoteApp.models import Rooms,Devices,Command, Users


class Api(APIView):
    def get(self,request):

        return Response(self.a)


class RoomsView(APIView):

    def get(self,request):
        rooms=Rooms.objects.all()
        roomSerializer=RoomsSerializer(rooms, many=True)

        response=Response(roomSerializer.data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class Register(APIView):
    parser_classes = (JSONParser,)

    def get(self, request):

        print(request.GET)
        return Response("aaa")

    def post(self, request):
        response=Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            user=Users()
            user.username=request.data["username"]
            user.login=request.data["login"]
            user.password=md5(bytes(request.data["password"],encoding='utf-8')).hexdigest()
            email=request.data["email"]
            if(not validate_email(email)):
                response.status_code=406
                response["Status"]="Invalid email"
                response.data={"detail":"Не правильный email"}

            user.email=email
            user.phone=request.data["phone"]
            user.save()
            response.data="register success"

        except KeyError:
            response.status_code = 400
            response["Status"] = "Incomplete data"
            response.data = {"detail": "Данные не полны"}

        return response


class Login(APIView):
    parser_classes = (JSONParser,)
    def post(self, request):
        response=Response()

        return response



class DeviceView(APIView):

    parser_classes = (JSONParser,)

    permission_classes = (AuthPermissions,)
    def get(self, request,id):
        response = Response()


        device=None
        command=None
        try:
            device=Devices.objects.get(id=id)

            command=Command.objects.filter(device=device)
        except ObjectDoesNotExist:


            response.status_code = 400
            response["Status"] = "Device not found"
            response.data={"detail":"Устройство не найдено"}
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
                response["Status"]= "Command not found"
                responseъ.data={"detail":"Такой команды нет у данного устройства"}
                return response

            commandSucces=command.setValue(value)

            if(commandSucces):
                response.status_code=202
                response.data={"detail":"Команда добавлена"}
            else:
                response.status_code=412
                response["Status"]="invalid value"
                response.data={"detail":"Недопустмое значение"}



        except ObjectDoesNotExist:

            response.status_code = 400
            response["Status"] ="Device is not founs"
            response.data="Устройство не найдено"

        except ValueError:
            response.status_code=400
            response["Status"]="Value must be integer"
            response.data={"detail":"Значение должно быть целым числом"}

        except KeyError:
            response.status_code=400
            response["Status"]="Incomplete data"
            response.data={"detail":"Данные не полны"}

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
            response.data={"detail":"Устройство создано"}
            return response
        except ValueError:
            response.status_code=400
            response["Status"]="roomId is not integer"
            response.data={"detail":"Значение должно быть целым числом"}
            return response
        except KeyError:
            response.status_code=400
            response["Status"]="Incomplete data"
            response.data={"detail":"Неполные данные"}
            return response

