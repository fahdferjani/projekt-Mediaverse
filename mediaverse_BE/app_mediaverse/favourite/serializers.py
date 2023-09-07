from rest_framework import serializers
from core.models import FavouriteList, FavouriteItem, Resource
from resource.serializers import ResourceSerializer

class FavouriteListSerializer(serializers.ModelSerializer):
    """Serializer for favourite lists."""

    class Meta:
        model = FavouriteList
        fields = ['id', 'user', 'title']
        read_only_fields = ['id', 'user']

class FavouriteItemSerializer(serializers.ModelSerializer):
    """Serializer for favourite items."""

    class Meta:
        model = FavouriteItem
        fields = ['id', 'favourite_list', 'resource', 'share']
        read_only_fields = ['id', 'favourite_list']

    def create(self, validated_data):
        favourite_list = validated_data['favourite_list']
        resource = validated_data['resource']

        # Check if the item already exists in the list
        if FavouriteItem.objects.filter(favourite_list=favourite_list, resource=resource).exists():
            raise serializers.ValidationError('Item already added to the favorite list')

        return super().create(validated_data)


class SharedListSerializer(serializers.ModelSerializer):
    """Serializer for shared favourite lists."""

    shared_items = serializers.SerializerMethodField()

    class Meta:
        model = FavouriteList
        fields = ['id', 'title', 'shared_items']

    def get_shared_items(self, obj):
        shared_items = obj.items.filter(share=True)
        resource_ids = shared_items.values_list('resource', flat=True)
        shared_resources = Resource.objects.filter(id__in=resource_ids)
        return ResourceSerializer(shared_resources, many=True).data

