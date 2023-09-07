import tempfile
import os


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Resource

from resource.serializers import (
    ResourceSerializer,
    ResourceDetailSerializer,
)
resource_list_url = reverse('resource:resource-list')
Resources_URL = resource_list_url.replace('all-', '')  # Remove the 'all-' prefix from the URL


def detail_url(resource_id):
    """Create and return a resource detail URL."""
    return reverse('resource:resource-detail', args=[resource_id])
def create_resource(user, **params):
    """Create and return a sample resource."""
    defaults = {
        'title':'Sample resource name',
        'author':'John Doe',
        'year':'2022',
        'description':'blablabla',
        'link':'https://example.com/resource',
        'code':'ABC123',
        'is_available_to_borrow':True,
    }
    defaults.update(params)
    resource = Resource.objects.create(user=user, **defaults)
    return resource

def create_user(**params):
    """Create and return a new user."""
    user = get_user_model().objects.create_user(**params)
    user.is_active = True
    user.is_mediathekar = True
    return user


class PublicresourceAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(Resources_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateResourceeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='Test Name', email='test@example.com', password='test-user-password123')
        self.client.force_authenticate(self.user)

    def test_retrieve_resources(self):
        """Test retrieving a list of resources."""
        create_resource(user=self.user)


        res = self.client.get(Resources_URL)

        resources = Resource.objects.all().order_by('-id')
        serializer = ResourceSerializer(resources, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_resource_successful(self):
        """Test creating a new resource."""
        payload = {
            'title': 'Sample resource name',
            'author': 'John Doe',
            'year': '2022',
            'description': 'Sample description',
            'link': 'https://example.com/resource',
            'code': 'ABC123',
        }
        res = self.client.post(Resources_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        resource = Resource.objects.get(id=res.data['id'])
        for key in payload:
            self.assertEqual(payload[key], getattr(resource, key))



    def test_create_resource_only_mediathekar(self):
        """Test that only Mediathekar users can create resources."""
        user = create_user(username='Regular User', email='regular@example.com', password='regular-user-password123')
        user.is_mediathekar = False
        self.client.force_authenticate(user)

        payload = {
            'title': 'Sample resource name',
            'author': 'John Doe',
            'year': '2022',
            'description': 'Sample description',
            'link': 'https://example.com/resource',
            'code': 'ABC123',
            'is_available_to_borrow': True,
        }
        res = self.client.post(Resources_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Resource.objects.filter(title=payload['title']).exists())


    def test_view_resource_detail(self):
        """Test viewing a resource detail."""
        resource = create_resource(user=self.user)

        url = detail_url(resource.id)
        res = self.client.get(url)

        serializer = ResourceDetailSerializer(resource)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


def test_delete_resource(self):
    """Test deleting a resource."""
    resource = create_resource(user=self.user)
    url = detail_url(resource.id)  # Use the detail URL for the specific resource
    res = self.client.delete(url)

    self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(Resource.objects.filter(id=resource.id).exists())




def test_update_resource(self):
    """Test updating a resource."""
    resource = create_resource(user=self.user)
    payload = {
        'title': 'Updated resource title',
        'author': 'Updated author name',
            'year': '2023',
            'description': 'Updated description',
            'link': 'https://example.com/updated-resource',
            'code': 'DEF456',
    }
    url = detail_url(resource.id)
    res = self.client.patch(url, payload)

    resource.refresh_from_db()
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    for key in payload:
        self.assertEqual(payload[key], getattr(resource, key))