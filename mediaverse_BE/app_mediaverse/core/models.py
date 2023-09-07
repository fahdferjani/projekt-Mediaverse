"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from datetime import date
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, email, password=None,  **extra_fields):
        """Create, save and return a new user."""
        if not username:
            raise ValueError('User must have a username.')
        if not email:
            raise ValueError('User must have an email.')
        user = self.model(username = username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.name = username
        user.save(using=self._db)

        return user

    def create_superuser(self,username,password, email = 'admin@example,com'):
        """Create and return a new superuser."""
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_mediathekar = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_mediathekar = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'


def resource_file_path(instance, filename):
    """Generate file path for a resource."""
    return f'resources/{instance.id}/{filename}'

year_CHOICES = [(str(i), str(i)) for i in range(1800, 2025)]

class Category(models.Model):
    """Category for filtering resources."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Type(models.Model):
    """Type for filtering resources."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Resource(models.Model):
    """Resource object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, default='')
    year = models.CharField(max_length=4, choices=year_CHOICES, blank=True, default='')
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True, default='')
    code = models.CharField(max_length=255, blank=True, default='')
    is_available_to_borrow = models.BooleanField(default=True)
    is_available_to_download = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category')
    types = models.ManyToManyField('Type')
    file = models.FileField(upload_to=resource_file_path, blank=True, null=True)

    def __str__(self):
        return self.title

    def is_available(self):
        """Check if the resource is available for borrowing."""
        return self.is_available_to_borrow and not BorrowTransaction.objects.filter(resource=self, returned=False).exists()

    def borrow(self, user,borrow_date , due_date):
        """Borrow the resource."""
        if self.is_available():
            self.is_available_to_borrow = False
            self.save()
            BorrowTransaction.objects.create(user=user, resource=self, borrow_date=borrow_date, due_date=due_date)

    def get_actual_borrowed_resources(self):
        """Get the actual borrowed resources for this resource."""
        return BorrowTransaction.objects.filter(resource=self, returned=False)

    def get_previous_borrowed_resources(self):
        """Get the previous borrowed resources for this resource."""
        return BorrowTransaction.objects.filter(resource=self, returned=True)



class BorrowTransaction(models.Model):
    """Borrow transaction object."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    number_of_extends = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"

    def extend_due_date(self, new_due_date):
        """Extend the due date of the borrow transaction."""
        if self.number_of_extends < 1:  # Check if the borrow has been extended less than 1 time
            self.due_date = new_due_date
            self.number_of_extends += 1  # Increment the number of extends
            self.save()
        else:
            raise ValidationError("Cannot extend the borrow more than once.")

    def return_resource(self):
        """Mark the resource as returned."""
        self.returned = True
        self.save()

    def return_resource(self):
        """Mark the resource as returned."""
        if self.returned:
            raise ValidationError("Resource is already marked as returned.")

        self.returned = True
        self.save()



class FavouriteList(models.Model):
    """Favourite list for users."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favourite_list'
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class FavouriteItem(models.Model):
    """Favourite item within a user's favourite list."""
    favourite_list = models.ForeignKey(
        FavouriteList,
        on_delete=models.CASCADE,
        related_name='items'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='favourite_items'
    )
    share = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.favourite_list.title} - {self.resource.title}"
