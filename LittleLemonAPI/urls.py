from django.urls import path, include
from . import views
    

urlpatterns = [
    path("", include('djoser.urls')),
    path("", include('djoser.urls.authtoken')),
    
    path("menu-items", views.MenuItemsListCreateAPIView.as_view()),
    path("menu-items/<int:pk>", views.MenuItemsRetrieveUpdateDestroyAPIView.as_view()),
    
    path("groups/manager/users", views.ManagersListCreateAPIView.as_view()),
    path("groups/manager/users/<int:pk>", views.ManagersDestoryAPIView.as_view()),
    
    path("groups/delivery-crew/users", views.DeliveryCrewListCreateAPIView.as_view()),
    path("groups/delivery-crew/users/<int:pk>", views.DeliveryCrewDestoryAPIView.as_view()),
    
    path("cart/menu-items", views.CartListCreateDestroyAPIView.as_view()),
 
    path("orders", views.OrderListCreateAPIView.as_view()),
    path("orders/<int:pk>", views.CustomerOrderRetrieveUpdateAPIView.as_view()),
]