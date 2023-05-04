from .models import MenuItem, Cart, Order, OrderItem, Category
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        depth = 1
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ["user"]
        depth = 1


class CartCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        unit_price = self.validated_data['menuitem'].price
        price = unit_price * self.validated_data['quantity']
        new_cart = Cart.objects.create(unit_price=unit_price,
                                       price=price, 
                                       user=self.validated_data['user'],
                                       menuitem=self.validated_data['menuitem'],
                                       quantity=self.validated_data['quantity'])
        return new_cart

    class Meta:
        model = Cart
        fields = ('menuitem', 'quantity', "user")
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields = ["user", "menuitem"]
            )            
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'menuitem', 'quantity', 'unit_price', 'price')
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')