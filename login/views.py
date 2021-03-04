from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from login.serializers import LoginSerializer, RegisterSerializer, ForGetPassWordSerializer, ResetPassWordSerializer
from login.utils.permissions import EmailTokenPermissions
from login.utils.tasks import send_email


from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from datetime import datetime, timedelta
import jwt

from account.utils.decorators import api_authenticate

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



# First call this api to set seesion and csrf key
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
                return Response(data = 'nog login')
                # raise APIException('02', '0001', '401', f'{user}')
            


# Forget password word to send email
class ForgetPassWordView(APIView):
    serializer_class = ForGetPassWordSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]

    def email_token(self, email):
        # Create payload
        payload = {
            'email': email, 
            'exp': int((datetime.now() + timedelta(minutes=10)).timestamp())
        }
        # Generate jwt token
        email_token = jwt.encode(
            payload, 
            settings.SECRET_KEY, # signature 
            algorithm="HS256"
        )
        return email_token


    @swagger_auto_schema(
        operation_summary = 'apply for account',
        manual_parameters = [
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
        if serializer.is_valid(raise_exception=True):
            to_email = serializer.data['email']
            html_msg = f'''
                <p>
                    Hello! Please enter to following link to reset password .
                    <a href ="http://127.0.0.1:8000/api/blog/class/?token={self.email_token(to_email)}">Link<a>
                </p>
            '''
            send_email.delay(
                subject = 'Music Reset Password Validation',  
                message = 'Email reset password',
                from_email = settings.EMAIL_HOST_USER,
                to_email = to_email,
                html_msg= html_msg
            )
        return Response('Email has been sent to your email', status = status.HTTP_200_OK)



# Reset Password after forgetting password     
class ResetPassWordView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPassWordSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [EmailTokenPermissions] # Custom permission class to verify that token is valid

    @swagger_auto_schema(
        operation_summary = 'apply for account',
        manual_parameters = [
            openapi.Parameter(
                'Authorization', 
                in_ = openapi.IN_HEADER,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'Token'
            ),
            openapi.Parameter(
                'email',
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'email'
            ),
            openapi.Parameter(
                'password',
                in_ = openapi.IN_FORM,
                type = openapi.TYPE_STRING,
                required = True,
                description = 'passwrod'
            ),
        ]
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_queryset().get(email = request.data['email'])
        serializer = self.serializer_class(
            user,
            data = request.data, 
            partial = True
        )
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        return Response('Update your password successfully', status = status.HTTP_200_OK)



class LogOutView(APIView):
    
    @api_authenticate((1, 2))
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(data = "You've benn logout")