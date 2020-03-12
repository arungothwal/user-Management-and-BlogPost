from django.http import Http404
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Function for custom exception handle"""
    response = exception_handler(exc, context)
    if isinstance(exc, Http404):
        response.data = {
            'message': 'No data available'  # custom exception message
        }
        return response
    try:
        print("Exception", exc.get_codes())
        if 'email' in exc.get_codes() and 'unique' in exc.get_codes()['email']:
            response.data = {
                'message': 'This email already exists.'  # custom exception message
            }
            return response
        if 'mobile_number' in exc.get_codes() and 'unique' in exc.get_codes()['mobile_number']:
            response.data = {
                'message': 'This mobile number already exists.'  # custom exception message
            }
            return response
        if 'dev_id' in exc.get_codes() and 'unique' in exc.get_codes()['dev_id']:
            response.data = {
                'message': 'This device already registered with other account.'  # custom exception message
            }
            return response
        return response
    except:
        return response