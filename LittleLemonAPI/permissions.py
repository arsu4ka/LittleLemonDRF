from rest_framework.permissions import BasePermission
from rest_framework.request import Request

class IsManager(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user and request.user.groups.filter(name="Manager").exists())

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name="delivery").exists())