from rest_framework.permissions import BasePermission


class AuthPermissions(BasePermission):


    def has_permission(self, request, view):
        print(request)
        return True

