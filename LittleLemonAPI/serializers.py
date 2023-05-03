from .models import MenuItem, Cart
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


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
        uint_price = self.validated_data['menuitem'].price
        price = uint_price * self.validated_data['quantity']
        new_cart = Cart.objects.create(uint_price=uint_price,
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
