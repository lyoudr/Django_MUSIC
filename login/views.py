from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# first call this api to set seesion and csrf key
@csrf_exempt
@api_view(['POST'])
def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        data = {
            'username': user.username,
            'id': user.id
        }
        return Response(data = data, status = status.HTTP_200_OK)
    else:
        # Return an 'invalid login' error message.
        return Response('wrong username or password', status = status.HTTP_401_UNAUTHORIZED)


def logout_view(request):
    logout(request)