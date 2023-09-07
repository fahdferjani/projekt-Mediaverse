"""
Serializers for resouce APIs
"""
from rest_framework import serializers

from core.models import Resource, Category, Type




class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories."""

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class TypeSerializer(serializers.ModelSerializer):
    """Serializer for types."""

    class Meta:
        model = Type
        fields = ['id', 'name']
        read_only_fields = ['id']

class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for resources."""
    # one resource can have many categories and types
    categories = CategorySerializer(many=True, required=False)
    types = TypeSerializer(many=True, required=False)
    is_available_to_borrow = serializers.BooleanField(read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'author', 'year', 'link', 'code','categories','types', 'is_available_to_borrow', 'file','description'
        ]
        read_only_fields = ['id']

    def _get_or_create_categories(self, categories, resource):
        """Handle getting or creating categories as needed."""
        auth_user = self.context['request'].user
        for cat in categories:
            cat_obj, created = Category.objects.get_or_create(
                user=auth_user,
                **cat,
            )
            resource.categories.add(cat_obj)
    def _get_or_create_types(self, types, resource):
        """Handle getting or creating categories as needed."""
        auth_user = self.context['request'].user
        for typ in types:
            typ_obj, created = Type.objects.get_or_create(
                user=auth_user,
                **typ,
            )
            resource.types.add(typ_obj)

    def create(self, validated_data):
        """Create a resource."""
        categories = validated_data.pop('categories', [])
        types = validated_data.pop('types', [])
        file = validated_data.pop('file', None)
        resource = Resource.objects.create(**validated_data)
        if file:
            resource.file = file
        self._get_or_create_categories(categories, resource)
        self._get_or_create_types(types, resource)
        return resource


    def update(self, instance, validated_data):
        """Update resource."""
        categories = validated_data.pop('categories', None)
        types = validated_data.pop('types', None)
        file = validated_data.pop('file', None)
        if categories is not None:
            instance.categories.clear()
            self._get_or_create_categories(categories, instance)
        if types is not None:
            instance.types.clear()
            self._get_or_create_categories(types, instance)

        if file:
            instance.file = file

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance




class ResourceDetailSerializer(ResourceSerializer):
    """Serializer for resource detail view."""

    class Meta(ResourceSerializer.Meta):
        fields = ResourceSerializer.Meta.fields + ['description']

