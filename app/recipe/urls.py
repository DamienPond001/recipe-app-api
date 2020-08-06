from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# DefaultRouter - feature that will auto generate the urls for ViewSet

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
