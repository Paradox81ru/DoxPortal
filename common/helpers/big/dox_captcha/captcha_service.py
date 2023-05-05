from django.http.response import HttpResponse
from rest_framework.request import HttpRequest

from common.helpers.big.dox_captcha.captcha import Captcha
from common.helpers.big.dox_captcha.captcha_redis_repository import CaptchaRedisRepository
from common.helpers.small.dox_utils import get_unique_hash_page
from common.helpers.small.singleton import MetaSingleton
from django.conf import settings

from datetime import datetime


class CaptchaService(metaclass=MetaSingleton):
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

    def remove_captcha_request(self, request: HttpRequest):
        """ Удаляет каптчу по запросу """
        unique_id = get_unique_hash_page(request)
        self.remove_captcha_unique_id(unique_id)

    def remove_captcha_unique_id(self, unique_id: str):
        """ Удаляет каптчу по ХЭШ-сумме url """
        self.captcha_repository.remove_captcha(unique_id)

    def add_failure_validate(self, request: HttpRequest):
        """ Увеличивает количество неудачных попыток ввода каптч """
        unique_id = get_unique_hash_page(request)
        self.captcha_repository.add_failure_validate(unique_id)

    def is_show_captcha(self, unique_id):
        """ Нужно ли отображать каптчу """
        number_failed_validate = getattr(settings, "NUMBER_FAILED_VALIDATE", 3)
        # Если количество неудачных входов больше указанных,
        if self.captcha_repository.get_failure_validate_value(unique_id) > number_failed_validate:
            # Узнаю, прошло ли время счётчика неудачных входов.
            time_elapsed_failure_validate = self.is_elapsed_time_failure_validate(unique_id)
            # Если времени счётчика неудачных входов нет,
            if time_elapsed_failure_validate is None:
                # значит каптчу отображать не надо.
                return False
            # Иначе, если время неудачных входов истекло,
            if time_elapsed_failure_validate:
                # значит удаляем счетчик неудачных входов,
                self.remove_captcha_unique_id(unique_id)
                # и каптчу отображать не будем.
                return False
            # Иначе надо отображать каптчу.
            return True
        return False

    def is_elapsed_time_failure_validate(self, unique_id):
        """ Проверяет, прошло ли время неудачных входов """
        time_elapsed_failure_validate = self.captcha_repository.get_captcha_counter_elapsed_time(unique_id)
        return self.is_time_expired(time_elapsed_failure_validate) if time_elapsed_failure_validate is not None else None

    @classmethod
    def is_time_expired(cls, date_time: datetime) -> bool:
        """ Проверят просрочено ли время """
        return datetime.now() > date_time
