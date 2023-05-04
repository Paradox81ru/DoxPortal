from datetime import datetime

from common.helpers.big.dox_captcha.captcha_redis_repository import \
    CaptchaRedisRepository, FailureCounterCaptchaRecord, CaptchaRecord
from common.helpers.small.dox_redis import redis
from common.helpers.small.dox_utils import get_unique_hash_page


def test_captcha(fake_http_request):
    """ Тестирует добавление каптчи """
    hash_url = get_unique_hash_page(fake_http_request)
    captcha_redis_repository = CaptchaRedisRepository()
    # Проверяет, что каптчи в хранилище ещё нет.
    assert not redis.hexists(CaptchaRedisRepository.DOX_CAPTCHA_KEY, hash_url)
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
    # Проверяем что установлена дата окончания действия каптчи.
    elapsed_time = captcha_redis_repository.get_captcha_elapsed_time(hash_url)
    assert isinstance(elapsed_time, datetime)

    # Удаляем каптчу из хранилища,
    captcha_redis_repository.remove_captcha(hash_url)
    # и проверяем, что каптча не найдена.
    assert not redis.hexists(CaptchaRedisRepository.DOX_CAPTCHA_KEY, hash_url)


def test_failure_validate(fake_http_request):
    hash_url = get_unique_hash_page(fake_http_request)
    captcha_redis_repository = CaptchaRedisRepository()
    # Проверяем, что неудачных попыток в хранилище ещё нет,
    assert not redis.hexists(CaptchaRedisRepository.DOX_FAILURE_COUNTER_CAPTCHA_KEY, hash_url)
    # и количество неудачных попыток соответственно 0.
    assert captcha_redis_repository.get_failure_validate_value(hash_url) == 0
    # Добавляем количество неудачных попыток
    captcha_redis_repository.add_failure_validate(hash_url)
    # и проверяем что увеличилось на единицу.
    assert captcha_redis_repository.get_failure_validate_value(hash_url) == 1
    # Ещё увеличиваем количество неудачных попыток,
    captcha_redis_repository.add_failure_validate(hash_url)
    # и вновь проверяем увеличение.
    assert captcha_redis_repository.get_failure_validate_value(hash_url) == 2
    # Проверяем, что установлена дата время окончания действия счётчика
    counter_elapsed_time = captcha_redis_repository.get_captcha_counter_elapsed_time(hash_url)
    assert isinstance(counter_elapsed_time, datetime)
    assert isinstance(captcha_redis_repository.get_failure_counter_captcha(hash_url), FailureCounterCaptchaRecord)


def teardown_module(module):
    CaptchaRedisRepository().remove_captcha_repository()
