from django.contrib.auth import get_user_model

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
        model = get_user_model() # get user model class
        #fields to convert to json
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