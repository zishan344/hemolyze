from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserDetailsViewSet
from blood_request.views import BloodRequestViewSet, AcceptBloodRequestViewSet

router = DefaultRouter()
router.register('user-details', UserDetailsViewSet, basename='user-details')
router.register('blood-request', BloodRequestViewSet, basename='blood-request')
router.register('accept-blood-request', AcceptBloodRequestViewSet, basename='accept-blood-request')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]