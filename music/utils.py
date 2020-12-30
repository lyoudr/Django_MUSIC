from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    '''
        1. exc : is the exception to be handled
        2. context : is a dictionary containing any extra context such as the view currently being handled.
    '''
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    return response

