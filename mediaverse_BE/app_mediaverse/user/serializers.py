"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from core.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    password2 = serializers.CharField(write_only=True,required = False)
    email = serializers.EmailField(required=False)
    is_mediathekar = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    #password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = get_user_model()
        fields = ['username','email', 'password', 'password2', 'is_mediathekar', 'is_staff']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def validate(self, attrs):
        """Validate the password fields."""
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        email =attrs.get('email')

        if password1 != password2:
            msg = _('passwords are not identical.')
            raise serializers.ValidationError(msg, code='Validation')

        if User.objects.filter(email=email).exists():
            msg = _('Email address is already in use.')
            raise serializers.ValidationError(msg, code='Validation')

        return attrs

    def create(self, validated_data):
        """Create and return a user with an encrypted password."""
        validated_data.pop('password2')
        validated_data.pop('is_mediathekar', None)
        validated_data.pop('is_staff', None)

        if not 'email' in validated_data:
            msg = _('you must provide an email.')
            raise serializers.ValidationError(msg, code='Validation')

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return the user."""
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)


       # Check if the email field has changed
        #if 'email' in validated_data and validated_data['email'] == instance.email:
         #   validated_data.pop('email')

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


    #---------------------------



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

