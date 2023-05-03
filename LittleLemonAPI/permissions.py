from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from LittleLemon.settings import MANAGER_GROUP_NAME, DELIVERY_CREW_GROUP_NAME


class IsManager(BasePermission):
    def has_permission(self, request: Request, view):
        
        return bool(request.user and request.user.groups.filter(name=MANAGER_GROUP_NAME).exists())

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name=DELIVERY_CREW_GROUP_NAME).exists())