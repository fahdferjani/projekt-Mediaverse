from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.models import FavouriteList, FavouriteItem
from .serializers import FavouriteListSerializer, FavouriteItemSerializer, SharedListSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes

class FavouriteListViewSet(viewsets.ModelViewSet):
    """ViewSet for managing favourite lists."""

    serializer_class = FavouriteListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve favourite lists for authenticated user."""
        return FavouriteList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new favourite list for the authenticated user."""
        serializer.save(user=self.request.user)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'shared',
                OpenApiTypes.STR,
                description='true or false',
            ),
        ]
    )
)
class FavouriteItemViewSet(viewsets.ModelViewSet):
    """ViewSet for managing favourite items."""

    serializer_class = FavouriteItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve favourite items for authenticated user with optional filtering."""
        queryset = FavouriteItem.objects.filter(favourite_list__user=self.request.user)

        # Check if 'shared' query parameter is provided
        shared = self.request.query_params.get('shared')
        if shared:
            if shared.lower() == 'true':
                queryset = queryset.filter(share=True)
            elif shared.lower() == 'false':
                queryset = queryset.filter(share=False)

        return queryset

    def perform_create(self, serializer):
        """Create a new favourite item."""
        favourite_list = FavouriteList.objects.get(user=self.request.user)
        resource = serializer.validated_data['resource']

        # Check if the item already exists in the list
        if FavouriteItem.objects.filter(favourite_list=favourite_list, resource=resource).exists():
            raise ValidationError('Item already added to the favorite list')

        serializer.save(favourite_list=favourite_list)



class SharedListViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving shared favourite lists."""

    serializer_class = SharedListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve shared favourite lists."""
        return FavouriteList.objects.filter(items__share=True)