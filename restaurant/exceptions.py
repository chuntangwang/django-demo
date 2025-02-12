from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import Error


def custom_exception_handler(exc, context):
    """
    Custom exception handler of rest_framework to handle internal server errors.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # handle exceptions are raised by Django, not DRF
    if response is None:
        if isinstance(exc, APIException):
            detail = exc.detail
        elif isinstance(exc, Error):
            # subclass of django.db.utils.Error
            detail = f'{exc}'
        elif hasattr(exc, 'message'):
            detail = [exc.message]
        elif hasattr(exc, 'messages'):
            detail = exc.messages
        else:
            # subclass of django.db.models.base.subclass_exception created at runtime
            message = exc.args[0] if len(exc.args) > 0 else str(exc.__class__)
            detail = f'{message}'
        response = Response(
            {'detail': detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
