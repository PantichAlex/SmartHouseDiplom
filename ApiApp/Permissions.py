from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from RemoteApp.models import Users


class AuthPermissions(BasePermission):


    def has_permission(self, request, view):
       # print(request.META["HTTP_AUTHORIZATION"].split()[1])
        return True

class UsersPermissinos(BasePermission):

    def has_permission(self, request, view):

        try:
            token=request.META["HTTP_AUTHORIZATION"]
            user=Users.objects.get(token=token)
            return True
        except ObjectDoesNotExist:
            return False
        except KeyError:
            return False

class UserPermissinos(BasePermission):

    def has_permission(self, request, view):

        try:
            token=request.META["HTTP_AUTHORIZATION"]
            user=Users.objects.get(token=token)

            return True
        except ObjectDoesNotExist:
            return False
        except KeyError:
            return False