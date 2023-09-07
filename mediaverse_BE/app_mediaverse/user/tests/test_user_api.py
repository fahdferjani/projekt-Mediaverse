"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    params.pop('password2')
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'username': 'test user',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_username_exists_error(self):
        """Test error returned if user with username exists."""
        payload = {
            'username': 'test user',
            'email': 'newemail@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            #'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'username': 'new user',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            #'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



    def test_password_too_short_error(self):
        """Test an error is returned if password less than 6 chars."""
        payload = {
            'username': 'test user',
            'email': 'test@example.com',
            'password': 'pw',
            'password2': 'pw',
            #'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

    def test_passwords_not_identical(self):
        """Test an error is returned if passwords not identical"""
        payload = {
            'username': 'test user',
            'email': 'test@example.com',
            'password': '1234567',
            'password2': '12345678',
            #'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_non_active_user(self):
        """Test returns error for valid credentials which were not activated by admin."""
        user_details = {
            'username': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
            'password2': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'username': user_details['username'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_for_activated_user(self):
        """Test returns error for valid credentials which were not activated by admin."""
        self.user = create_user(
            username= 'test user',
            email='test@example.com',
            password='testpass123',
            password2='testpass123',
            is_active=True,
        )
        self.client = APIClient()
        payload = {
            'username': 'test user',
            'password': 'testpass123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)




    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(username='user1',email = 'user@example,com', password='goodpass', password2='goodpass',is_active=True)

        payload = {'username':'user2', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given username."""
        payload = {'username':'userx', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'username':'userx', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            username= 'test user',
            email='test@example.com',
            password='testpass123',
            password2='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'username': self.user.username,
            'email': self.user.email,
            'is_mediathekar' : self.user.is_mediathekar,
            'is_staff': self.user.is_staff,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'username':self.user.username , 'email': 'Updatedname@example.com', 'password': 'newpassword123', 'password2': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

