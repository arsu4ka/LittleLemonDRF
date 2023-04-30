from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDeliveryCrew, IsManager
from .models import MenuItem
from django.contrib.auth.models import User, Group
from .serializer import MenuItemSerializer, UserSerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "POST":
            permission_classes += [IsManager]
        return [permission() for permission in permission_classes]

    
class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method != "GET":
            permission_classes += [IsManager]
        return [permission() for permission in permission_classes]
    

class ManagersView(APIView):
    permission_classes = [IsManager]
    
    def get(self, request: Request):
        manager_group = Group.objects.get(name='Manager')
        managers = User.objects.filter(groups__name=manager_group.name)
        managers_serializer = UserSerializer(managers, many=True)
        return Response(managers_serializer.data)