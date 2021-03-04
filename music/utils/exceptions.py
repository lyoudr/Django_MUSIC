from rest_framework.views import exception_handler
from rest_framework.response import Response

class DBError :

    def get_db_error_msg(self, err_code, obj_name):
        if err_code == '0001':
            return f'{obj_name} can not be found .'
        if err_code == '0002':
            return f'{obj_name} can not be created .'
        if err_code == '0003':
            return f'{obj_name} can not be updated .'
        if err_code == '0004':
            return f'{obj_name} can not be deleted .'
    
class APIError :

    def get_api_error_msg(self, err_code, obj_name):
        if err_code == '0001':
            return f'{obj_name} is not authorized.'
        if err_code == '0002':
            return f'{obj_name} is forbidden to this api.'
        if err_code == '0003':
            return f'{obj_name} can not be updated .'
        if err_code == '0004':
            return f'{obj_name} can not be deleted .'

class SYSError :

    def get_sys_error_msg(self, err_code, obj_name):
        if err_code == '0001':
            return f'{obj_name} can not be found .'
        if err_code == '0002':
            return f'{obj_name} can not be created .'
        if err_code == '0003':
            return f'{obj_name} can not be updated .'
        if err_code == '0004':
            return f'{obj_name} can not be deleted .'




class Error(DBError, APIError, SYSError) :
    def __init__(self):
        self.err_list = {
            '01': 'DB_ERROR',
            '02': 'API_ERROR',
            '03': 'SYS_ERROR'
        }


    def error_result(self, err_num, err_code, obj_name):
        
        err_name = self.err_list.get(err_num)

        if err_name == 'DB_ERROR':
            err_msg = self.get_db_error_msg(err_code, obj_name)

        if err_name == 'API_ERROR':
            err_msg = self.get_api_error_msg(err_code, obj_name)

        if err_name == 'SYS_ERROR':
            err_msg = self.get_sys_error_msg(err_code, obj_name)

        print('err_msg is =>', err_msg)
        return {
            'error' : f'{err_name}',
            'code': f'{err_num}-{err_code}',
            'message': err_msg
        }






def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    response = exception_handler(exc, context)
    err_type, err_code, status_code, obj_name = exc.args
    err_handler = Error()
    error_result = err_handler.error_result(err_type, err_code, obj_name)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error_result'] = error_result

    return Response(data = error_result, status = status_code)
