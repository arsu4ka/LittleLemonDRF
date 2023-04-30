from .models import MenuItem
from django.contrib.auth.models import User
from rest_framework import serializers


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login", "date_joined", "user_permissions", "groups"]