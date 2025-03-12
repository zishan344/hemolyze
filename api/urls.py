from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter
from djoser import views as djoser_views
from rest_framework_nested.routers import NestedDefaultRouter
from user.views import UserDetailsView

router = DefaultRouter()
router.register(r'users', djoser_views.UserViewSet, basename='user')
users_router = NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'details', UserDetailsView, basename='user-details')

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('auth/', include(users_router.urls)),
    path('', include(router.urls)),
]