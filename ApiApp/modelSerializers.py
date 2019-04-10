
from rest_framework.serializers import ModelSerializer

from RemoteApp.models import Rooms, Devices,Users,Macro,Premissions


class RoomsSerializer(ModelSerializer):
    class Meta:
        model=Rooms
        fields=('RoomName', 'Description')

class DeviceSerializer(ModelSerializer):
    class Meta:
        model=Devices
        fields = ("id","name", "driverPath", "iconPath", "template", "room")

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
