from collections import namedtuple
from typing import Final
from django.conf import settings

from common.helpers.small.dox_redis import redis
from datetime import datetime, timedelta

from django.core.serializers.json import DjangoJSONEncoder
import json

CaptchaRecord = namedtuple("CaptchaRecord", ["text", "elapsed_time"])


# class CaptchaRecord:
#     def __init__(self, text: str, time_elapsed_failure_validate: datetime | str):
#         self._text = text
#         if isinstance(time_elapsed_failure_validate, datetime):
#             self._time_elapsed_failure_validate: datetime = time_elapsed_failure_validate
#         elif isinstance(time_elapsed_failure_validate, str):
#             self._time_elapsed_failure_validate: datetime = datetime.strptime(time_elapsed_failure_validate, '%d.%m.%Y %H:%M:%S')
#         else:
#             raise TypeError(f"Invalid date-time type {time_elapsed_failure_validate.__class__.__name__}")
#
#         self._time_elapsed_failure_validate: datetime = \
#             time_elapsed_failure_validate if isinstance(time_elapsed_failure_validate, datetime) \
#             else datetime.strptime(time_elapsed_failure_validate, '%d.%m.%Y %H:%M:%S')
#
#     @property
#     def text(self):
#         return self._text
#
#     @property
#     def time_elapsed_failure_validate(self):
#         return self._time_elapsed_failure_validate
#
#     @property
#     def time_elapsed_failure_validate_str(self):
#         return datetime.strftime(self._time_elapsed_failure_validate, '%d.%m.%Y %H:%M:%S')


class CaptchaRedisRepository:
    """ Хранилища каптчи """
    DOX_CAPTCHA_KEY: Final = "dox_captcha_dj"
    DOX_FAILURE_COUNTER_CAPTCHA_KEY: Final = "dox_failure_counter_captcha_dj"

    def add_captcha(self, text: str, unique_id: str):
        wait_reset_failed_validate: Final = getattr(settings, "WAIT_RESET_FAILED_VALIDATE", 30)
        time_elapsed_failure_validate = datetime.now() + timedelta(minutes=wait_reset_failed_validate)
        redis.hset(self.DOX_CAPTCHA_KEY, unique_id, CaptchaRecord(text, time_elapsed_failure_validate))
