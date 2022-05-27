from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
