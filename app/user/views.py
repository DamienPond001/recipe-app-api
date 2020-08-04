from user.serializers import UserSerializer

from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """create a new user"""
    serializer_class = UserSerializer