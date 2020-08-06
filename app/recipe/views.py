from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

# mixins add functionality to the base class
class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the db"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    #queryset is what we want to return
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for current authed user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet, 
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """manage ingredients in the db"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """return objects for crrent user"""

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """create new ingredient"""
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in db"""

    # the ModelViewSet class knows how to create a new instance as long as 
    # we provide a serialiser that is attached to a model. We just need 
    # assign the authed user to that model
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returve user recipes"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """return appropriate serialiser class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """create new recipe"""
        serializer.save(user=self.request.user)


# class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
#                             mixins.ListModelMixin,
#                             mixins.CreateModelMixin):
#     """Base viewset for user owned recipe attributes"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')

#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)


# class TagViewSet(BaseRecipeAttrViewSet):
#     """Manage tags in the database"""
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer


# class IngredientViewSet(BaseRecipeAttrViewSet):
#     """Manage ingredients in the database"""
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer
