"""
Views for the resources APIs
"""
from rest_framework import status
from django.http import HttpResponse
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from core.models import Resource, Category, Type
from resource import serializers


class IsMediathekar(BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if user is registered as Mediathekar
        return request.user.is_mediathekar



@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'categories',
                OpenApiTypes.STR,
                description='Comma separated list of categories IDs to filter',
            ),
            OpenApiParameter(
                'types',
                OpenApiTypes.STR,
                description='Comma separated list of types IDs to filter',
            ),
        ]
    )
)

class ResourceViewSet(viewsets.ModelViewSet):
    """
    View for manage resource APIs.
    Defining operations to manage resources.
    """
    serializer_class = serializers.ResourceDetailSerializer
    queryset = Resource.objects.all()
    authentication_classes = [TokenAuthentication]
    # only mediathekar(or admin) can manage resources
    permission_classes = [IsAuthenticated, IsMediathekar]


    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]


    ##every user can only get and update his own resouces(created by him).
    #def get_queryset(self):
    #    """Retrieve resources for authenticated user."""
    #    return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_queryset(self):
        """
        Retrieve resources for authenticated user.
        Filtering by categories and types.
        """
        categories = self.request.query_params.get('categories')
        types = self.request.query_params.get('types')
        queryset = self.queryset
        if categories:
            cat_ids = self._params_to_ints(categories)
            queryset = queryset.filter(categories__id__in=cat_ids)
        if types:
            types_ids = self._params_to_ints(types)
            queryset = queryset.filter(types__id__in=types_ids)
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()


    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ResourceSerializer
        return self.serializer_class


    def perform_create(self, serializer):
        # Create a new resource and mark it as created by the user.
        serializer.save(user=self.request.user)


    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download the resource file."""
        resource = self.get_object()
        if resource.file:
            file_path = resource.file.path
            file_name = resource.file.name.split('/')[-1]
            # get the file from the path and return it as a response
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CategoryViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Manage categories in the database."""
    # make it possible to manage categories
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMediathekar]



class TypeViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Manage types in the database."""
    # make it possible to manage types
    serializer_class = serializers.TypeSerializer
    queryset = Type.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMediathekar]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'categories',
                OpenApiTypes.STR,
                description='Comma separated list of categories IDs to filter',
            ),
            OpenApiParameter(
                'types',
                OpenApiTypes.STR,
                description='Comma separated list of types IDs to filter',
            ),
            OpenApiParameter(
                'code',
                OpenApiTypes.STR,
                description='a code to look for',
            ),
            OpenApiParameter(
                'title',
                OpenApiTypes.STR,
                description='give the title you are searching',
            ),
            OpenApiParameter(
                'year',
                OpenApiTypes.STR,
                description='give the year you are searching',
            ),
            OpenApiParameter(
                'author',
                OpenApiTypes.STR,
                description='give the author you are searching',
            ),
            OpenApiParameter(
                'is_available',
                OpenApiTypes.STR,
                description='is_available to borrow ?',
            ),
        ]
    )
)

class AllResourcesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving all resources.
    allows authenticated users to search for resources with read only permission.
    and filter them by categories and types.
    """

    serializer_class = serializers.ResourceDetailSerializer
    queryset = Resource.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def _params_to_strings(self, qs):
        """Convert a list of params to string."""
        return [code for code in qs.split(',')]

    def get_queryset(self):
        """Retrieve resources for authenticated user with the filtering."""
        categories = self.request.query_params.get('categories')
        types = self.request.query_params.get('types')
        code = self.request.query_params.get('code')
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')
        is_available = self.request.query_params.get('is_available')
        queryset = self.queryset
        if title:  #Perform search by title
            queryset = queryset.filter(title__icontains=title)
        if year:  #Perform search by year
            queryset = queryset.filter(year__icontains=year)
        if author:  #Perform search by author
            queryset = queryset.filter(author__icontains=author)
        if categories:
            cat_ids = self._params_to_ints(categories)
            queryset = queryset.filter(categories__id__in=cat_ids)
        if types:
            type_ids = self._params_to_ints(types)
            queryset = queryset.filter(types__id__in=type_ids)
        if code:
            code_list = self._params_to_strings(code)
            queryset = queryset.filter(code__in=code_list)
        if is_available:
            queryset = queryset.filter(is_available_to_borrow=True)
        return queryset.order_by('-id').distinct()
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ResourceSerializer
        return self.serializer_class



class AllCategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving all categories.
    allows users to search for categories with read only permission.
    """

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AllTypesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving all categories.
    allows users to search for types with read only permission.
    """

    serializer_class = serializers.TypeSerializer
    queryset = Type.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
