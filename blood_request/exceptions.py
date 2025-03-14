from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        return Response({
            'error': exc.message
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return exception_handler(exc, context)