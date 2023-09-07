"""
URL mappings for the resource app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from resource import views


router1 = DefaultRouter()
router1.register('resources', views.ResourceViewSet)
router1.register('categories', views.CategoryViewSet)
router1.register('types', views.TypeViewSet)
router1.register('all-resources', views.AllResourcesViewSet)
router1.register('all-categories', views.AllCategoriesViewSet)
router1.register('all-types', views.AllTypesViewSet)

app_name = 'resource'

urlpatterns = [
    path('', include(router1.urls)),
]