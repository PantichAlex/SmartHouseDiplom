
from rest_framework.serializers import ModelSerializer

from RemoteApp.models import Rooms, Devices,Users,Macro,Premissions,Command, CommandType


class RoomsSerializer(ModelSerializer):
    class Meta:
        model=Rooms
        fields=('RoomName', 'Description')

class DeviceSerializer(ModelSerializer):
    class Meta:
        model=Devices
        fields = ("id","name", "driverPath", "iconPath", "template", "room")


class CommandTypeSerializer(ModelSerializer):
    class Meta:
        model=CommandType
        fields=("typeName","desMin","desMax")



class RemoteDevicePanelSerializer(ModelSerializer):
    ctype = CommandTypeSerializer()
    class Meta:
        model=Command
        fields=("name","ctype" ,"value", "minValue","maxValue","description")


class UserSerializer(ModelSerializer):
    class Meta:
        model=Users
        fields=("username")

class PermissionSeralizer(ModelSerializer):
    class Meta:
        model=Premissions
        fields = ("Description","device")

class MacroSerializer(ModelSerializer):
    class Meta:
        model=Macro
        fields = ("user","device", "text")
# Register your models here.
