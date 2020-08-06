from django.contrib.auth import get_user_model, authenticate

#This allows for easy translation, just by passing strings through it
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


# ModelSerializer is a built in class that helps serialise db items
# it handles the various processes involved in retrieving db items
# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    # need to create the Meta class. Meta classes are used for 'runtime'
    # config that is not of db concern
    # Here is is used to establish which model and fields to serialize
    class Meta:
        model = get_user_model()  # get user model class
        # fields to convert to json
        fields = ('email', 'password', 'name')

        # Other validators
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """create new user"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user and setting password, and return"""
        # instance is the model instance
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)  # use default update on the rest
        if password:
            user.set_password(password)
            user.save()

        return user


# This is largely based off the TokenSerializer that comes with django
# We need to modify to allow for email instead of username
class AuthTokenSerializer(serializers.Serializer):
    """Serialzer for user auth object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # This is what is called when we validate
    def validate(self, attrs):
        """Validate and suthenicate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        # As we pass the serializer into the ViewSet, the REST Framework
        # passes the context into the serializer as a 'context' class variable
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

