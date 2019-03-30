from django.contrib import admin
from .models import Rooms,Users,Premissions, UserPemissions, Devices, Macro


@admin.register(Rooms)
class RoomAdmin(admin.ModelAdmin):
    fields = ("RoomName","Description")

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    fields=("username","login", "password", "email", "phone")

@admin.register(Premissions)
class PermissionAdmin(admin.ModelAdmin):
    fields = ("Description","device")


@admin.register(UserPemissions)
class UserPermissiosAdmin(admin.ModelAdmin):
    fields = ("user", "permission")


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    fields=("name", "driverPath", "iconPath", "template", "room")

@admin.register(Macro)
class MacroAdmin(admin.ModelAdmin):
    fields = ("user","device", "text")
# Register your models here.
