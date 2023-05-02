from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager
from .models import MenuItem, Cart
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer

MANAGER_GROUP = Group.objects.get(pk=1)
DELIVERY_CREW = Group.objects.get(pk=2)

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
    queryset = User.objects.filter(groups=MANAGER_GROUP)
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(groups=[MANAGER_GROUP])


class DestroyManagerView(views.APIView):
    permission_classes = [IsManager]
    
    def delete(self, pk: int):
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"message": "couldn't find user with given id"}, status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(MANAGER_GROUP)
        user.save(force_update=True)
        return Response(UserSerializer(user).data, status.HTTP_200_OK)


class DeliveryCrewsView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups=DELIVERY_CREW)
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(groups=[DELIVERY_CREW])
        
        
class DestroyDeliveryCrewView(views.APIView):
    permission_classes = [IsManager]
    
    def delete(self, pk: int):
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"message": "couldn't find user with given id"}, status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(DELIVERY_CREW)
        user.save(force_update=True)
        return Response(UserSerializer(user).data, status.HTTP_200_OK)


class CartListCreateDeleteView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        quantity = serializer.validated_data['quantity']
        menu_item = serializer.validated_data['menuitem']
        serializer.validated_data['total_price'] = quantity * menu_item.price
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)