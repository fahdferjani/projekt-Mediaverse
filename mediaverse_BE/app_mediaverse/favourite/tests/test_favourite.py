from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import FavouriteList, FavouriteItem, Resource
from favourite.serializers import FavouriteListSerializer, FavouriteItemSerializer

FAVOURITE_LISTS_URL = reverse('favourite:favourite-list-list')
FAVOURITE_ITEMS_URL = reverse('favourite:favourite-item-list')

def create_user(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**params)

def create_favourite_list(user, title):
    """Helper function to create a favourite list."""
    return FavouriteList.objects.create(user=user, title=title)

def create_favourite_item(favourite_list, resource, share=False):
    """Helper function to create a favourite item."""
    return FavouriteItem.objects.create(favourite_list=favourite_list, resource=resource, share=share)

class FavouriteListApiTests(TestCase):
    """Test the favourite list API."""

    def setUp(self):
        self.user = create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_favourite_list(self):
        """Test creating a new favourite list."""
        payload = {'title': 'Books'}
        res = self.client.post(FAVOURITE_LISTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        favourite_list = FavouriteList.objects.get(id=res.data['id'])
        self.assertEqual(favourite_list.user, self.user)
        self.assertEqual(favourite_list.title, payload['title'])

def test_list_favourite_lists(self):
    """Test listing favourite lists for the authenticated user."""
    create_favourite_list(user=self.user, title='Books')
    create_favourite_list(user=self.user, title='Movies')

    res = self.client.get(FAVOURITE_LISTS_URL)

    favourite_lists = FavouriteList.objects.filter(user=self.user)
    serializer = FavouriteListSerializer(favourite_lists, many=True)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)

class FavouriteItemApiTests(TestCase):
    """Test the favourite item API."""

    def setUp(self):
        self.user = create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.favourite_list = create_favourite_list(user=self.user, title='Books')
        self.resource1 = Resource.objects.create(user=self.user, title='Book 1')
        self.resource2 = Resource.objects.create(user=self.user, title='Book 2')

    def test_create_favourite_item(self):
        """Test creating a new favourite item."""
        payload = {
            'favourite_list': self.favourite_list.id,
            'resource': self.resource1.id,
            'share': False
        }
        res = self.client.post(FAVOURITE_ITEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        favourite_item = FavouriteItem.objects.get(id=res.data['id'])
        self.assertEqual(favourite_item.favourite_list, self.favourite_list)
        self.assertEqual(favourite_item.resource, self.resource1)
        self.assertEqual(favourite_item.share, False)

    def test_list_favourite_items(self):
        """Test listing favourite items for the authenticated user."""
        create_favourite_item(favourite_list=self.favourite_list, resource=self.resource1)
        create_favourite_item(favourite_list=self.favourite_list, resource=self.resource2)

        res = self.client.get(FAVOURITE_ITEMS_URL)

        favourite_items = FavouriteItem.objects.filter(favourite_list=self.favourite_list)
        serializer = FavouriteItemSerializer(favourite_items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_duplicate_favourite_item(self):
        """Test creating a duplicate favourite item."""
        create_favourite_item(favourite_list=self.favourite_list, resource=self.resource1)

        payload = {
            'favourite_list': self.favourite_list.id,
            'resource': self.resource1.id,
            'share': False
        }
        res = self.client.post(FAVOURITE_ITEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class SharedListApiTests(TestCase):
    """Test the shared favourite list API."""

    def setUp(self):
        self.user = create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.favourite_list = create_favourite_list(user=self.user, title='Books')
        self.resource = Resource.objects.create(user=self.user, title='Book 1')
        create_favourite_item(favourite_list=self.favourite_list, resource=self.resource, share=True)

    def test_list_shared_lists(self):
        """Test listing shared favourite lists."""
        url = reverse('favourite:shared-resources-list')
        res = self.client.get(url)

        shared_lists = FavouriteList.objects.filter(items__share=True)
        serializer = FavouriteListSerializer(shared_lists, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

