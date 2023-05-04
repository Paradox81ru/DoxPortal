import pickle

from common.helpers.big.dox_captcha.captcha_redis_repository import CaptchaRedisRepository, CaptchaRecord
from common.helpers.small.dox_utils import get_unique_hash_page
from common.helpers.small.dox_redis import redis

from datetime import datetime

import pytest


# def test_captcha_record_class():
#     """ Тестирует класс CaptchaRecord """
#     date_time = datetime(2023, 5, 3, 16, 40, 0)
#     captcha_record = CaptchaRecord("test", date_time)
#     assert captcha_record.time_elapsed_failure_validate_str == "03.05.2023 16:40:00"
#     date_time_str = "30.04.2023 10:20:00"
#     captcha_record = CaptchaRecord("test", date_time_str)
#     assert captcha_record.time_elapsed_failure_validate == datetime(2023, 4, 30, 10, 20, 0)
#     with pytest.raises(TypeError, match="Invalid date-time type int") as err:
#         captcha_record = CaptchaRecord("test", 1234567)


def test_add_captcha(fake_http_request):
    """ Тестирует добавление каптчи """
    hash_url = get_unique_hash_page(fake_http_request)
    captcha_redis_repository = CaptchaRedisRepository()
    # Добавляет каптчу в хранилище.
    captcha_redis_repository.add_captcha("text", hash_url)
    # Проверяет, что каптча была добавлена.
    assert redis.hexists(CaptchaRedisRepository.DOX_CAPTCHA_KEY, hash_url)

    # Вытаскиваем запись каптчи,
    captcha_record: CaptchaRecord = captcha_redis_repository.get_captcha(hash_url)
    # и проверяем, что тип каптчи верный.
    assert isinstance(captcha_record, CaptchaRecord)

    # Проверяем текст каптчи.
    assert captcha_redis_repository.get_text(hash_url) == "text"

    # Удаляем каптчу из хранилища,
    captcha_redis_repository.remove_captcha(hash_url)
    # и проверяем, что каптча не найдена.
    assert not redis.hexists(CaptchaRedisRepository.DOX_CAPTCHA_KEY, hash_url)


def teardown_module(module):
    redis.delete(CaptchaRedisRepository.DOX_CAPTCHA_KEY)