from django.conf import settings

from rest_framework import permissions

from datetime import datetime, timedelta
import jwt


class EmailTokenPermissions(permissions.BasePermission):
    '''
    Check for email token
    '''
    def has_permission(self, request, view):
        email_token = request.headers.get('Authorization')
        print('email_token is =>', email_token)
        # decode token
        try:
            payload = jwt.decode(email_token, settings.SECRET_KEY, algorithms='HS256')
            print('payload is =>', payload)
            # varify token is not expired
            if int(datetime.now().timestamp()) >= payload['exp']:
                print("here")
                return False
            else:
                return True
        except :
            return False
