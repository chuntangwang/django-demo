from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.serializers import CharField, ListField
from rest_framework.settings import api_settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from restaurant.authentication import CsrfExemptSessionAuthentication
from restaurant import serializers
from drf_spectacular.utils import extend_schema, inline_serializer


detail_serializer = inline_serializer(
    name='DetailResponse', fields={'detail': CharField()}
)

errors_serializer = inline_serializer(
    name='ErrorsResponse',
    fields={
        api_settings.NON_FIELD_ERRORS_KEY: ListField(),
    },
)

empty_serializer = inline_serializer(name='EmptySerializer', fields={})


class RegisterView(CreateAPIView):
    """
    Register a new user.
    """

    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]
    response_serializer = {201: serializers.UserSerializer, 400: errors_serializer}

    @extend_schema(
        auth=[],
        request=serializers.UserSerializer,
        responses=response_serializer,
        tags=['Login'],
    )
    def post(self, request):
        try:
            validate_password(request.data['password'])
        except ValidationError as e:
            return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'username': user.username, 'email': user.email},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(CreateAPIView):
    """
    Login with username and password.
    """

    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]
    request_serializer = inline_serializer(
        name='LoginRequest', fields={'username': CharField(), 'password': CharField()}
    )
    response_serializer = {
        201: inline_serializer(
            name='LoginResponse',
            fields={'detail': CharField(), 'session_id': CharField()},
        ),
        400: detail_serializer,
    }

    @extend_schema(
        auth=[],
        request=request_serializer,
        responses=response_serializer,
        tags=['Login'],
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            session_id = request.session.session_key
            return Response(
                {
                    'detail': f'{request.user.username} successfully logged in.',
                    'session_id': session_id,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    'detail': 'Invalid credentials.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class AuthTokenView(CreateAPIView):
    """
    Create or update the auth token of session user.
    """

    permission_classes = [IsAuthenticated]
    response_serializer = {
        200: inline_serializer(name='TokenRequest', fields={'token': CharField()}),
        401: detail_serializer,
    }

    @extend_schema(
        request=empty_serializer, responses=response_serializer, tags=['Authorization']
    )
    def post(self, request):
        token, _ = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key})


class LogoutView(DestroyAPIView):
    """
    Logout the current user.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @extend_schema(auth=[], responses={204: detail_serializer}, tags=['Authorization'])
    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
