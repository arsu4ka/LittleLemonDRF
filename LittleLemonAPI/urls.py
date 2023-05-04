from django.urls import path, include
from . import views
    

urlpatterns = [
    path("", include('djoser.urls')),
    path("", include('djoser.urls.authtoken')),
    
    path("menu-items", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.MenuItemView.as_view()),
    
    path("groups/manager/users", views.ManagersView.as_view()),
    path("groups/manager/users/<int:pk>", views.DestroyManagerView.as_view()),
    
    path("groups/delivery-crew/users", views.DeliveryCrewsView.as_view()),
    path("groups/delivery-crew/users/<int:pk>", views.DestroyDeliveryCrewView.as_view()),
    
    path("cart/menu-items", views.CartListCreateDestroyAPIView.as_view()),
 
    path("orders", views.OrderListCreateAPIView.as_view()),
    path("orders/<int:pk>", views.CustomerOrderRetrieveAPIView.as_view()),
]