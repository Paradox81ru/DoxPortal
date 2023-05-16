from django.http import HttpRequest
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from common.helpers.big.dox_captcha.captcha_service import CaptchaService

def custom_exception_handler(exc: ValidationError, context):
    """ Собственный обработчик исключений """
    # Сначала вызовите обработчик исключений REST framework по умолчанию,
    # чтобы получить стандартный ответ об ошибке.
    response = exception_handler(exc, context)

    # Теперь добавьте код состояния HTTP в ответ.
    if response is not None and exc.__class__.__name__ != 'AuthenticationFailed':
        response.data['fields_error'] = exc.detail.copy()
        response.data['status_cose'] = response.status_code
        if context.get('request').path == '/api/auth/login':
            response.data['isShowCaptcha'] = CaptchaService().is_show_captcha(context.get('request'))
        response.data['error'] = exc.__class__.__name__
    # if exc.__class__.__name__ == 'AuthenticationFailed':
    #     response.data['login_data'] = get_login_data(None, '')

    return response
