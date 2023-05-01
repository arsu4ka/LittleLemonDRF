from django.urls import path, include
from .views import MenuItemsView, MenuItemView, ManagersView, DestroyManagerView, DeliveryCrewsView, DestroyDeliveryCrewView

urlpatterns = [
    path("", include('djoser.urls')),
    path("", include('djoser.urls.authtoken')),
    
    path("menu-items", MenuItemsView.as_view()),
    path("menu-items/<int:pk>", MenuItemView.as_view()),
    
    path("groups/manager/users", ManagersView.as_view()),
    path("groups/manager/users/<int:pk>", DestroyManagerView.as_view()),
    
    path("groups/delivery-crew/users", DeliveryCrewsView.as_view()),
    path("groups/delivery-crew/users/<int:pk>", DestroyDeliveryCrewView.as_view()),
]