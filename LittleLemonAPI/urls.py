from django.urls import path, include
from .views import MenuItemsView

urlpatterns = [
    path("", include('djoser.urls')),
    path("", include('djoser.urls.authtoken')),
    path("menu-items", MenuItemsView.as_view())
]