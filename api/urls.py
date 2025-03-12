from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter
from djoser import views as djoser_views
from rest_framework_nested.routers import NestedDefaultRouter
from user.views import UserDetailsView

# Main router for future viewsets (not for users)
router = DefaultRouter()

# User router specifically for auth endpoints
user_router = DefaultRouter()
user_router.register(r'users', djoser_views.UserViewSet, basename='user')

users_router = NestedDefaultRouter(user_router, r'users', lookup='user')
users_router.register(r'details', UserDetailsView, basename='user-details')


urlpatterns = [
    # Authentication and user routes under auth/
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('auth/', include(user_router.urls)),
    # path('auth/', include(users_router.urls)),
    
    # Keep this for future non-user routers
    path('', include(router.urls)),
]