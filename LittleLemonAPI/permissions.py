from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .constants import get_manager_group, get_delivery_crew_group


class IsManager(BasePermission):
    def has_permission(self, request: Request, view = None):
        return bool(request.user and request.user.groups.filter(pk=get_manager_group().pk).exists())

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view = None):
        return bool(request.user and request.user.groups.filter(pk=get_delivery_crew_group().pk).exists())
    
class IsWorker(BasePermission):
    def has_permission(self, request, view = None):
        return bool(request.user and (request.user.groups.filter(pk=get_delivery_crew_group().pk).exists() or request.user.groups.filter(pk=get_manager_group().pk).exists()))