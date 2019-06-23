
from rest_framework.serializers import ModelSerializer

from RemoteApp.models import Rooms, Devices,Users,Macro,Premissions,Command, CommandType


class RoomsSerializer(ModelSerializer):
    class Meta:
        model=Rooms
        fields=('id','RoomName', 'Description')

class DeviceSerializer(ModelSerializer):
    room=RoomsSerializer()
    class Meta:
        model=Devices
        fields = ("id","name", "driverPath", "iconPath", "room")


class CommandTypeSerializer(ModelSerializer):
    class Meta:
        model=CommandType
        fields=("typeName","desMin","desMax")



class RemoteDevicePanelSerializer(ModelSerializer):
    ctype = CommandTypeSerializer()
    class Meta:
        model=Command
        fields=("id","name","ctype" ,"value", "minValue","maxValue","description")


class UserSerializer(ModelSerializer):
    class Meta:
        model=Users
        fields=("id","username","email","phone","admin")


class PermissionSeralizer(ModelSerializer):
    class Meta:
        model=Premissions
        fields = ("id","Description","device","read","write")

class UserPermissionsSerializer(ModelSerializer):
    permissions=PermissionSeralizer(many=True)
    class Meta:
        model=Users
        fields = ("id", "username", "email", "phone", "admin","permissions")


class MacroSerializer(ModelSerializer):
    class Meta:
        model=Macro
        fields = ("user","device", "text")

class UserTokenSerializer(ModelSerializer):
    class Meta:
        model=Users
        fields=("token","refreshToken")
# Register your models here.
