from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .mixins import SerializerByMethodMixin
from .permissions import IsManager
from .models import MenuItem, Cart, Order, OrderItem
from .constants import get_manager_group, get_delivery_crew_group
from django.contrib.auth.models import User
from django.db.models import Sum
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, CartCreateSerializer, OrderItemSerializer, OrderSerializer


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
    queryset = User.objects.filter(groups=get_manager_group())
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(groups=[get_manager_group()])


class DestroyManagerView(views.APIView):
    permission_classes = [IsManager]
    
    def delete(self, request, pk: int):
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"message": "couldn't find user with given id"}, status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(get_manager_group())
        user.save(force_update=True)
        return Response(UserSerializer(user).data, status.HTTP_200_OK)


class DeliveryCrewsView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups=get_delivery_crew_group())
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(groups=[get_delivery_crew_group()])
        
        
class DestroyDeliveryCrewView(views.APIView):
    permission_classes = [IsManager]
    
    def delete(self, pk: int):
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"message": "couldn't find user with given id"}, status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(get_delivery_crew_group())
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
        request.data["user"] = request.user.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class_by_method['get'](instance=instance).data, status=201)


class CustomerOrderListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data, status.HTTP_200_OK)
    
    
    # works well, but without serializer
    # 
    def post(self, request: Request):
        carts = Cart.objects.filter(user=request.user)
        
        order = Order.objects.create(
            user=request.user,
            total = carts.aggregate(Sum('price'))['price__sum'] or 0
        )
        
        for cart in carts:
            OrderItem.objects.create(
                order=order,
                menuitem = cart.menuitem,
                quantity = cart.quantity,
                unit_price = cart.unit_price,
                price = cart.price
            )
            
        carts.delete()
        return Response({"message": "success"}, status.HTTP_201_CREATED)