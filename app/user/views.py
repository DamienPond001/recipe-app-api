from user.serializers import UserSerializer, AuthTokenSerializer

from rest_framework import generics, authentication, permissions
# Note that if we didn't need to customise the email field, this could be 
# passed directly to urls
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """create a new user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token"""

    serializer_class = AuthTokenSerializer

    # Set the render so that we can view this endpoint in the browser
    # why is this done?
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer

    # authentication is mechanism by which auth happens
    authentication_classes = (authentication.TokenAuthentication,)
    # permissions are the level of access
    permission_classes = (permissions.IsAuthenticated,)

    # We need to add get object function to APIView
    def get_object(self):
        """retrieve and return authed user"""
        # The authentication classes take care of adding the user to the request
        return self.request.user
