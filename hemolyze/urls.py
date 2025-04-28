from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Define schema view with explicitly no authentication
schema_view = get_schema_view(
   openapi.Info(
      title="Hemolyze API",
      default_version='v1',
      description="API documentation for the Hemolyze blood donation platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@hemolyze.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(),  # Empty tuple means no authentication required
)

# Apply csrf_exempt to all schema view methods to bypass CSRF protection
schema_view = method_decorator(csrf_exempt, name='dispatch')(schema_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + debug_toolbar_urls()
