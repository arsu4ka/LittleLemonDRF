from .models import MenuItem, Cart
from django.contrib.auth.models import User
from rest_framework import serializers


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
        fields = ["menuitem", "quanity", "total_price"]
        read_only_fields = ["total_price"]