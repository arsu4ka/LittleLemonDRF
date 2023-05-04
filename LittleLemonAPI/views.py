from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .mixins import SerializerByMethodMixin
from .permissions import IsManager, IsDeliveryCrew, IsWorker
from .models import MenuItem, Cart, Order, OrderItem, Category
from .constants import get_manager_group, get_delivery_crew_group
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, CartCreateSerializer, OrderItemSerializer, OrderSerializer, CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    

class MenuItemsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        queryset = MenuItem.objects.all()
        if self.request.method != "GET":
            return queryset
        
        category_slug = self.request.query_params.get('category')
        to_price = self.request.query_params.get('to_price')
        from_price = self.request.query_params.get("from_price")
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if to_price:
            queryset = queryset.filter(price__lte=to_price)
        if from_price:
            queryset = queryset.filter(price__gte=from_price)
        return queryset
        
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "POST":
            permission_classes.append(IsManager)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        category_id = self.request.data.get("category")
        category = get_object_or_404(Category, pk=category_id)
        serializer.save(category=category)

    
class MenuItemsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method != "GET":
            permission_classes.append(IsManager)
        return [permission() for permission in permission_classes]
    

class ManagersListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsManager]
    
    def get(self, request: Request):
        managers = User.objects.filter(groups=get_manager_group())
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        username = request.data.get("username")
        if not username:
            return Response({"message": "'username' field required"}, status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=username)
        if not user.exists():
            return Response({"message": "user with given username wasn't found"}, status.HTTP_404_NOT_FOUND)
        
        user = user.first()
        user.groups.add(get_manager_group())
        user.save(force_update=True)
        return Response(UserSerializer(user).data, status.HTTP_200_OK)
        

class ManagersDestoryAPIView(generics.GenericAPIView):
    permission_classes = [IsManager]
    
    def delete(self, request, pk: int):
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"message": "couldn't find user with given id"}, status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(get_manager_group())
        user.save(force_update=True)
        return Response(UserSerializer(user).data, status.HTTP_200_OK)


class DeliveryCrewListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsManager]
    
    def get(self, request: Request):
        delivery_guys = User.objects.filter(groups=get_delivery_crew_group())
        serializer = UserSerializer(delivery_guys, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        username = request.data.get("username")
        if not username:
            return Response({"message": "'username' field required"}, status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=username)
        if not user.exists():
            return Response({"message": "user with given username wasn't found"}, status.HTTP_404_NOT_FOUND)
        
        user = user.first()
        user.groups.add(get_delivery_crew_group())
        user.save(force_update=True)
        return Response(UserSerializer(user).data, status.HTTP_200_OK)
        
        
class DeliveryCrewDestoryAPIView(generics.GenericAPIView):
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
 

class OrderListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if IsManager().has_permission(request):
            orders = Order.objects.all()
        elif IsDeliveryCrew().has_permission(request):
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
            
        serialized_orders = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            item_serializer = OrderItemSerializer(order_items, many=True)
            serialized_order = OrderSerializer(order).data
            serialized_order["order_items"] = item_serializer.data
            serialized_orders.append(serialized_order)
        return Response(serialized_orders, status=status.HTTP_200_OK)
    
    # works well, but without serializer
    def post(self, request: Request):
        carts = Cart.objects.filter(user=request.user)
        if not carts.exists():
            return Response({"message": "your cart is empy"}, status.HTTP_400_BAD_REQUEST)
        
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
    

class CustomerOrderRetrieveUpdateAPIView(generics.GenericAPIView):
    
    def get(self, request: Request, pk: int):
        order = Order.objects.filter(pk=pk).first()
        if not order or order.user != request.user:
            return Response({"message": "either this order doesn't exist or it's not yours"}, status.HTTP_400_BAD_REQUEST)
        
        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        serialized_order = OrderSerializer(order).data
        serialized_order["order_items"] = order_items_serializer.data
        return Response(serialized_order, status.HTTP_200_OK)
    
    def put(self, request: Request, pk: int):
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response({"message": "order with given id doesn't exist"}, status.HTTP_400_BAD_REQUEST)
        
        order_serializer = OrderSerializer(order, data=request.data, partial=True)
        order_serializer.is_valid(raise_exception=True)
        updated_order = order_serializer.save()
        return Response(OrderSerializer(updated_order).data, status.HTTP_200_OK)
    
    def patch(self, request: Request, pk: int):
        if IsManager().has_permission(request):
            return self.put(request, pk)
        
        try:
            new_status = request.data.get("status")
            if new_status == None:
                raise Exception()
            request.data = {"status": bool(new_status)}
            return self.put(request, pk)
        except:
            return Response({"message": "you can change only status of the order"}, status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request: Request, pk: int):
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response({"message": "order with given id doesn't exist"}, status.HTTP_400_BAD_REQUEST)
        
        orderitems = OrderItem.objects.filter(order=order)
        order.delete()
        orderitems.delete()
        return Response({"message": "success"}, status.HTTP_200_OK)
        
    def get_permissions(self):
        permissions = [IsAuthenticated]
        
        if self.request.method == "DELETE" or self.request.method == "PUT":
            permissions.append(IsManager)
        elif self.request.method == "PATCH":
            permissions.append(IsWorker)
        
        return [permission() for permission in permissions]