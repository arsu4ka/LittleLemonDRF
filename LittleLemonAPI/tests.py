from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch

from django.contrib.auth.models import User
from .models import MenuItem
from .constants import get_manager_group, get_delivery_crew_group


class MenuItemsListCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_item_data = {'name': 'Pizza', 'price': 10.99}

    def test_permissions(self):
        response = self.client.post('menu-items', data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_authenticate(user=User.objects.create(group=get_manager_group), token="testtoken")
        response = self.client.post('menu-items', data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MenuItemsRetrieveUpdateDestroyAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_item = MenuItem.objects.create(name='Burger', price=8.99)

    def test_permissions(self):
        response = self.client.get(reverse('menu-detail', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.put(reverse('menu-detail', args=[self.menu_item.id]), data={'name': 'New Burger', 'price': '9.99'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_authenticate(user=User.objects.create(username="manager"), token="testtoken")
        response = self.client.put(reverse('menu-detail', args=[self.menu_item.id]), data={'name': 'New Burger', 'price': '9.99'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('menu-detail', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_authenticate(user=User.objects.create(username="manager"), token="testtoken")
        response = self.client.delete(reverse('menu-detail', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
