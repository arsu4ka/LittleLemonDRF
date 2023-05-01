from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDeliveryCrew, IsManager
from .models import MenuItem
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, UserSerializer


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
    
    
class ManagersView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    manager_group = Group.objects.get(pk=1)
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(groups=[self.manager_group])

