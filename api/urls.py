from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserDetailsViewSet

router = DefaultRouter()
router.register('user-details', UserDetailsViewSet, basename='user-details')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]