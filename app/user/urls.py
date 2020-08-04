from django.urls import path

from user import views


app_name = 'user' # this is used to idenetify the app such as in 'reverse' fn

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
