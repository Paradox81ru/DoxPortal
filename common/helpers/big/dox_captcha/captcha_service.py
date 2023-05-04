from django.http.response import HttpResponse
from rest_framework.request import HttpRequest

from common.helpers.big.dox_captcha.captcha import Captcha
from common.helpers.big.dox_captcha.captcha_redis_repository import CaptchaRedisRepository
from common.helpers.small.dox_utils import get_unique_hash_page
from common.helpers.small.singleton import singleton


@singleton
class CaptchaService:
    """ Управление каптчей """
    def __init__(self):
        self.captcha_repository = CaptchaRedisRepository()

    def set_captcha(self, destination: HttpResponse, request: HttpRequest):
        """ Устанавливает каптчу """
        unique_id = get_unique_hash_page(request)
        captcha = Captcha().captcha(destination)
        self.captcha_repository.add_captcha(captcha, unique_id)

    def validate_captcha_request(self, text: str, request: HttpRequest):
        """ Проверяет текст каптчи из запроса """
        unique_id = get_unique_hash_page(request)
        return self.validate_captcha_unique_id(text, unique_id)

    def validate_captcha_unique_id(self, text: str, unique_id: str):
        """ Проверяет текст каптчи по ХЭШ-сумме url """
        text_captcha = self.captcha_repository.get_text(unique_id)
        return text_captcha is not None and text_captcha == text