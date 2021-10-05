from django.http import JsonResponse

from rest_framework import status
from rest_framework.exceptions import APIException

class CustomError(APIException):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'CustomError'
    default_code = 'CustomError'

    def __init__(self, return_code = None, status_code = None, return_message = None):
        if return_code is None:
            return_code = '9999'
        if return_message is None:
            return_message = 'unknow_err'
        if status_code is None:
            self.status_code = status_code
        
        self.detail = {
            'return_code': return_code,
            'return_message': return_message,
        }


class CustomJsonResponse(JsonResponse):
    """CustomJsonResponse

    An HTTP response class that inherits JsonResponse
    :param res: A named_tuple imported from ci_admin.results.code_n_msg
                and passed to pay_load.
    :param data: A dictionary of kwargs passed to pay_load.
    :param pagination: The response of ci_admin.pagination.CustomPagination

    """
    def __init__(self, return_code='0000', return_message='', result_data={}, pagination={}, **kwargs):

        self.data = self.set_payload(return_code, return_message, result_data, pagination)

        super(CustomJsonResponse, self).__init__(
            data=self.data,
            **kwargs
        )


    def set_payload(self, return_code='0000', return_message='', result_data={}, pagination={}):
        payload = {
            'return_code': return_code,
            'return_message': return_message,
            'result_data': result_data
        }
        
        if pagination:
            payload['pagination'] = pagination
        return payload