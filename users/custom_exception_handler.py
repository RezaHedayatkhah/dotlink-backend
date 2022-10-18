from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if exc.__class__.__name__ == 'AuthenticationFailed':
        response.data = {
            "status": "error",
            "message": "کاربری با این مشخصات یافت نشد"
        }
    if exc.__class__.__name__ == 'ValidationError':
        response.data = {
            "status": "error",
            "message": response.data
        }
    return response
    