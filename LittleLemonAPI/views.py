from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .models import MenuItem
from .serializer import MenuItemSerializer

class MenuItemsView(APIView):
    
    def get(self, request: Request):
        menu_items = MenuItem.objects.all()
        serialized_items = MenuItemSerializer(menu_items, many=True)
        return Response(serialized_items.data)