from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta
from core.models import Resource, BorrowTransaction

class BorrowResourceTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.user.is_active = True
        self.client.force_authenticate(user=self.user)
        self.resource = Resource.objects.create(
            user=self.user,
            title='Sample Resource',
            description='Sample resource description.',
            is_available_to_borrow=True,
            is_available_to_download=False,
        )

    def test_borrow_resource(self):
        url = reverse('borrow-resource', args=[self.resource.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowTransaction.objects.count(), 1)
        transaction = BorrowTransaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.resource, self.resource)
        self.assertFalse(transaction.returned)


    def test_borrow_resource_not_available(self):
        self.resource.is_available_to_borrow = False
        self.resource.save()

        url = reverse('borrow-resource', args=[self.resource.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BorrowTransaction.objects.count(), 0)


    def test_borrow_resource_invalid_resource(self):
        invalid_resource_id = 9999
        url = reverse('borrow-resource', args=[invalid_resource_id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(BorrowTransaction.objects.count(), 0)

    def test_borrow_resource_multiple_times(self):
        url = reverse('borrow-resource', args=[self.resource.id])

        # First borrow
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowTransaction.objects.count(), 1)

        # Second borrow
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BorrowTransaction.objects.count(), 1)



    def test_borrow_resource_transaction_details(self):
        url = reverse('borrow-resource', args=[self.resource.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction = BorrowTransaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.resource, self.resource)
        self.assertFalse(transaction.returned)
        self.assertEqual(transaction.due_date, date.today() + timedelta(days=14))


    def test_borrow_resource_returned_resource(self):
        self.resource.is_available_to_borrow = False
        self.resource.is_available_to_download = False
        self.resource.save()

        # Create a borrow transaction for the resource
        borrow_transaction = BorrowTransaction.objects.create(user=self.user, resource=self.resource,borrow_date=date.today(), due_date=date.today() + timedelta(days=14))

        url = reverse('borrow-resource', args=[self.resource.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BorrowTransaction.objects.count(), 1)
        self.assertEqual(borrow_transaction.returned, False)

    def test_borrow_resource_due_date(self):
        url = reverse('borrow-resource', args=[self.resource.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction = BorrowTransaction.objects.first()
        self.assertEqual(transaction.due_date, date.today() + timedelta(days=14))