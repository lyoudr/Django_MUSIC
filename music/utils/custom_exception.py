from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class CustomError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'CustommError'
    default_code = 'CustomError'
    
    def __init__(self, return_code = None, return_message = None, status_code = None):
        
        return_code = '9999' if return_code else None
        return_message = return_message if return_message else _('unkonw_err')
        self.status_code = status_code if status_code else None

        self.detail = {
            'return_code': return_code,
            'return_message': return_message
        }
