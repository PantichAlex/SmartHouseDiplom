from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from RemoteApp.models import Users,Devices


class AuthPermissions(BasePermission):


    def has_permission(self, request, view):
        try:
            token = request.META["HTTP_AUTHORIZATION"]
            user = Users.objects.get(token=token)
            if(request.method=="POST" or request.method=="DELETED"):
                return user.admin
            device=None
            try:
                devId=view.kwargs["id"]
                device=Devices.objects.get(id=devId)
            except ObjectDoesNotExist:
                return True
            answer=False
            userPermissions=user.permissions.filter(device=device)
            for permission in userPermissions:
                if(request.method=="GET"):
                    answer|=permission.read
                if(request.method=="PUT"):
                    answer|=permission.write

            return answer

        except ObjectDoesNotExist:
            return False
        except KeyError:
            return False


class UsersPermissinos(BasePermission):

    def has_permission(self, request, view):

        try:
            token=request.META["HTTP_AUTHORIZATION"]
            user=Users.objects.get(token=token)
            if (request.method == "GET"):
                return True

            return user.admin

        except ObjectDoesNotExist:
            return False
        except KeyError:
            return False

class UserPermissinos(BasePermission):

    def has_permission(self, request, view):

        try:
            token=request.META["HTTP_AUTHORIZATION"]
            user=Users.objects.get(token=token)
            if(request.method=="GET"):
                return True

            return user.admin
        except ObjectDoesNotExist:
            return False
        except KeyError:
            return False


class AdminPermissinos(BasePermission):

    def has_permission(self, request, view):

        try:
            token=request.META["HTTP_AUTHORIZATION"]
            user=Users.objects.get(token=token)

            return user.admin
        except ObjectDoesNotExist:
            return False
        except KeyError:
            return False