from rest_framework import generics, mixins
from rest_framework import status
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .mixins import SerializerByMethodMixin
from .permissions import IsManager
from .models import MenuItem, Cart
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, CartCreateSerializer

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


class CartListCreateDestroyAPIView(SerializerByMethodMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class_by_method = {
        'get': CartSerializer,
        'delete': CartSerializer,
        'post': CartCreateSerializer
    }

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get(self, request):
        instances = self.get_queryset()
        serializer = self.get_serializer(instance=instances, many=True)
        return Response(serializer.data)

    def delete(self, request):
        instances = self.get_queryset()
        instances.delete()
        return Response(status=202)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class_by_method['get'](instance=instance).data, status=201)
