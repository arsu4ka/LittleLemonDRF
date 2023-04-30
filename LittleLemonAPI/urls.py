from django.urls import path, include
from .views import MenuItemsView, MenuItemView

urlpatterns = [
    path("", include('djoser.urls')),
    path("", include('djoser.urls.authtoken')),
    path("menu-items", MenuItemsView.as_view()),
    path("menu-items/<int:pk>", MenuItemView.as_view()),
]