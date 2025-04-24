from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from user.views import UserDetailsViewSet,AllUserDetailsViewSet
from blood_request.views import BloodRequestViewSet, AcceptBloodRequestViewSet
from dashboard.views import DonarListViewSet, DonationHistoryViewSet

router = DefaultRouter()

router.register('user-details', UserDetailsViewSet, basename='user_details')
router.register("all-user-details", AllUserDetailsViewSet, basename="all_user_details")
router.register('blood-request', BloodRequestViewSet, basename='blood-request')

blood_router = routers.NestedDefaultRouter(router, 'blood-request', lookup='blood_request')
blood_router.register(
    'accept-blood-request',
    AcceptBloodRequestViewSet,
    basename='accept-blood-request'
)

# router.register('accept-blood-request', AcceptBloodRequestViewSet, basename='accept-blood-request')
router.register('donar-list', DonarListViewSet, basename='donar-list')
router.register('donation-history', DonationHistoryViewSet, basename='donation-history')
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('', include(blood_router.urls)),
    # path('', include(users_router.urls)),
]