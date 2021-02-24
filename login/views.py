from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from login.serializers import LoginSerializer, RegisterSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Register use , apply for an account
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = 'apply for account',
        manual_parameters = [
            openapi.Parameter(
                'username', 
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'username'
            ),
            openapi.Parameter(
                'password',
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'password'
            ),
            openapi.Parameter(
                'email',
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'email'
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        return Response(data = serializer.data, status = status.HTTP_200_OK)



# first call this api to set seesion and csrf key
class LogInView(GenericAPIView):
    serializer_class = LoginSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='login view',
        manual_parameters=[
            openapi.Parameter(
                'username',
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'username'
            ),
            openapi.Parameter(
                'password',
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'password'
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                request, 
                username = serializer.data['username'], 
                password = serializer.data['password']
            )
            if user is not None:
                login(request, user)
                # Generate token
                refresh = RefreshToken.for_user(user)
                # Redirect to a success page.
                data = {
                    'username': user.username,
                    'id': user.id,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                return Response(data = data, status = status.HTTP_200_OK)
            else:
                # Return an 'invalid login' error message.
                return Response('wrong username or password', status = status.HTTP_401_UNAUTHORIZED)


def logout_view(request):
    logout(request)