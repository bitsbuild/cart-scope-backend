from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user.views import create_user,delete_user
urlpatterns = [
    path('create/',create_user,name='create'),
    path("gettoken/",obtain_auth_token,name='gettoken'),
    path("delete/",delete_user,name='delete')
]
