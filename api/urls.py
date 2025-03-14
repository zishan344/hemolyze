from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserDetailsViewSet
from blood_request.views import BloodRequestViewSet, AcceptBloodRequestViewSet
from dashboard.views import DonarListViewSet, DonationHistoryViewSet

router = DefaultRouter()
router.register('user-details', UserDetailsViewSet, basename='user_details')
router.register('blood-request', BloodRequestViewSet, basename='blood-request')
router.register('accept-blood-request', AcceptBloodRequestViewSet, basename='accept-blood-request')
router.register('donar-list', DonarListViewSet, basename='donar-list')
router.register('donation-history', DonationHistoryViewSet, basename='donation-history')
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    # path('', include(users_router.urls)),
]