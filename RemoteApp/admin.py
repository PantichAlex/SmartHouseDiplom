from django.contrib import admin
from .models import Rooms,Users,Premissions, Devices, Macro, Command,CommandType


@admin.register(Rooms)
class RoomAdmin(admin.ModelAdmin):
    fields = ("RoomName","Description")

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    fields=("username","login", "password","permissions", "email", "phone","token","refreshToken", "admin")

@admin.register(Premissions)
class PermissionAdmin(admin.ModelAdmin):
    fields = ("Description","device","read","write")


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    fields=("name", "driverPath", "iconPath", "template", "room","deleted")

@admin.register(Macro)
class MacroAdmin(admin.ModelAdmin):
    fields = ("user","device", "text")


@admin.register(CommandType)
class CommandTypeAdmin(admin.ModelAdmin):
    fields = ("typeName","desMax", "desMin")

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    fields = ("name",  "ctype","driverIdenti","value","minValue", "maxValue","device","description")