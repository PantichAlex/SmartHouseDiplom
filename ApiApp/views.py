#-*-coding: utf-8 -*-

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist,PermissionDenied
from django.utils.decorators import method_decorator

from hashlib import md5,sha1
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from validate_email import validate_email

from .apiDecorators import auth
from .modelSerializers import RoomsSerializer, DeviceSerializer,RemoteDevicePanelSerializer,UserTokenSerializer,UserSerializer
from .Permissions import AuthPermissions,UsersPermissinos, UserPermissinos
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
            user.secretKey=sha1(bytes(str(request.data["secret_key"]),encoding='utf-8')).hexdigest()
            user.generateTokens()
            response.data={"succes":"Регистрация прошла"}
            response.status_code=201

        except KeyError:
            response.status_code = 400
            response["Status"] = "Incomplete data"
            response.data = {"detail": "Данные не полны"}

        except IntegrityError:
            response.status_code=403
            response["Status"]="This user be registered"
            response.data={"detail":"Пользователь уже существует"}

        return response

    def delete(self):
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            login = request.data["login"]
            password = request.data["password"]

            user = Users.objects.get(login=login)
            if(user.deleted):
                raise ObjectDoesNotExist()
            user.deleted=True
            response.status_code=202
            response.data={"succes":"Пользователь удален"}

        except PermissionDenied:
            response.status_code = 403
            response["Status"] = "Incorrect password"
            response.data = {"detail": "Неверный пароль"}
        except KeyError:
            response.status_code = 400
            response["Status"] = "Incomplete data"

            response.data = {"detail": "Данные не полны"}
        except ObjectDoesNotExist:
            response.status_code = 404
            response["Status"] = "User is not found"
            response.data = {"detail": "Пользователь не найден"}
        return response

    def put(self,request):
        response=Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            data=dict()
            login=request.data["login"]
            password=request.data["password"]
            user=Users.objects.get(login=login)
            if(not user.correctPassword(password)):
                raise PermissionDenied()
            if("new_password" in request.data):
                newPassword=request.data["new_password"]
                data["new_password"]=True
                user.changePassword(password, newPassword)
                user.generateTokens()
            else:
                data["new_password"]=False

            if("username" in request.data):
                username=request.data["username"]
                data["username"]=True
                user.username=username
            else:
                data["username"]=False

            if("phone" in request.data):
                phone=request.data["phone"]
                data["phone"]=True
                user.phone=phone
            else:
                data["phone"]=False

            if("email" in request.data):
                email=request.data["email"]
                if(validate_email(email)):
                    data["email"]=True
                    user.email=email
                else:
                    data["email"]=False
            else:
                data["email"]=False

            response.status_code=201
            response.data =data
            user.save()
        except PermissionDenied:
            response.status_code=403
            response["Status"]="Incorrect password"
            response.data={"detail":"Неверный пароль"}
        except KeyError:
            response.status_code = 400
            response["Status"] = "Incomplete data"

            response.data = {"detail": "Данные не полны"}
        except ObjectDoesNotExist:
            response.status_code=404
            response["Status"]="User is not found"
            response.data={"detail":"Пользователь не найден"}
        return response

class Login(APIView):
    parser_classes = (JSONParser,)
    def get(self, request):
        response=Response()
        response["Access-Control-Allow-Origin"] = "*"
        return response

    def post(self, request):
        response=Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            user=Users.objects.get(login=request.data["login"])
            if(user.deleted):
                response.status_code=401
                response["Status"]="User is deleted"
                response.data={"detail":"Пользователь был удален"}
                return response

            password = request.data["password"]
            if user.correctPassword(password):
                serializer=UserTokenSerializer(user)
                response.data=serializer.data
            else:
                response.status_code=403
                response["Status"]="Incorrect password"
                response.data={"detail":"Неверный пароль"}

        except KeyError:
            response.status_code=400
            response["Status"]="Incorrect auntification data"
            response.data={"detail":"Не устанновлены авторизационные данные"}
        except ObjectDoesNotExist:
            response.status_code=404
            response["Status"]="User is not found"
            response.data={"detail":"Пользователь не найден"}

        return response

    def put(self,request):
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            user = Users.objects.get(login=request.data["login"])
            if (user.deleted):
                response.status_code = 401
                response["Status"] = "User is deleted"
                response.data = {"detail": "Пользователь был удален"}
                return response
            secretKey=sha1(bytes(str(request.data["secret_key"]),encoding='utf-8')).hexdigest()
            if(user.secretKey!=secretKey):
                response.status_code=403
                response["Status"]="Secret key is incorrect"
                response.data={"detaill":"Секретный ключ не верен"}
                return response

            user.resetPassword()
            response.data={"success":"Новый пвроль выслан на почту"}
            return response

        except KeyError:
            response.status_code = 400
            response["Status"] = "Incorrect auntification data"
            response.data = {"detail": "Не передан логин"}
        except ObjectDoesNotExist:
            response.status_code = 404
            response["Status"] = "User is not found"
            response.data = {"detail": "Пользователь не найден"}

        return response

    def delete(self, request):
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            refreshToken=request.data["RefreshToken"]

            user=Users.objects.get(refreshToken=refreshToken)

            user.resetTokens(refreshToken)

            response.data="reset tokens success"
            return response
        except PermissionDenied:
            response.status_code=403
            response["Status"]="Incorrect RefreshToken"
            response.data={"detail":"Не верный обновляющий токен"}
        except KeyError:
            response.status_code=400
            response["Status"]="RefreshToken not found"
            response.data={"detail":"Не указан обновляющий токен"}
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
                response.dat={"detail":"Команда добавлена"}
            else:
                response.status_code=412
                response["Status"]="invalid value"
                response.data={"detail":"Недопустмое значение"}



        except ObjectDoesNotExist:

            response.status_code = 400
            response["Status"] ="Device is not founs"
            response.data={"detsil":"Устройство не найдено"}

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
            response.data={"succes":"Устройство создано"}
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

class UserView(APIView):
    parser_classes = (JSONParser,)
   # permission_classes = (UserPermissinos,)

    def get(self,request,id):
        response=Response()
        response["Access-Control-Allow-Origin"] = "*"
        try:
            user=Users.objects.get(id=id)
            permissions=PermissionModel.objects.filter(user=user)
            response.data=userPermissions.data
        except ObjectDoesNotExist:
            response.status_code=404
            response["Status"]="UserNotFound"
            response.data={"detail":"Пользователь не найден"}
        return response

class UsersView(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (UsersPermissinos,)

    def get(self,request):
        response=Response()
        response["Access-Control-Allow-Origin"] = "*"

        users = Users.objects.all()
        usersSerializer = UserSerializer(users, many=True)
        response.data = usersSerializer.data


        return response