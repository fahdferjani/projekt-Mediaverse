from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import FavouriteListViewSet, FavouriteItemViewSet, SharedListViewSet

router = DefaultRouter()
router.register(r'favourite-lists', FavouriteListViewSet, basename='favourite-list')
router.register(r'favourite-items', FavouriteItemViewSet, basename='favourite-item')
router.register('shared-resources', SharedListViewSet, basename='shared-resources')

app_name = 'favourite'
urlpatterns = [
    path('', include(router.urls)),
]
