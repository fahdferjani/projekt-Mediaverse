"""
Tests for models.
"""
#from unittest.mock import patch
#from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

#from core import models


def create_user(username = 'user', email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(username, email, password)



class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_username_successful(self):
        """Test creating a user with an email is successful."""
        username = 'test'
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com', 'test1'],
            ['Test2@Example.com', 'Test2@example.com','test2'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com','test3'],
            ['test4@example.COM', 'test4@example.com','test4'],
        ]
        for email, expected, username in sample_emails:
            user = get_user_model().objects.create_user(username, email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('user', '', 'test123')

    def test_new_user_without_username_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'user@example.com', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'adminn',
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_resource(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'use1',
            'test@example.com',
            'testpass123',
        )
        resource = models.Resource.objects.create(
            user=user,
            title='Sample resource name',
            description='Sample resource description.',
        )

        self.assertEqual(str(resource), resource.title)