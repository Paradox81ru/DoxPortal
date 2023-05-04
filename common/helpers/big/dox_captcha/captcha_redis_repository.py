import pickle
from collections import namedtuple
from datetime import datetime, timedelta
from typing import Final

from django.conf import settings

from common.helpers.small.dox_redis import redis

# Каптча [text: текст каптчи, elapsedTime: дата-время окончания действия каптчи]
CaptchaRecord = namedtuple("CaptchaRecord", ["text", "elapsed_time"])

# Количества неудачных попыток проверок каптч
# [counter: счётчик неудачных попыток, elapsedTime: дата-время окончания действия счётчика неудачных попыток]
FailureCounterCaptchaRecord = namedtuple("FailureCounterCaptchaRecord", ["counter", "elapsed_time"])


class CaptchaRedisRepository:
    """ Хранилище каптчи """
    DOX_CAPTCHA_KEY: Final = "dox_captcha_dj"
    DOX_FAILURE_COUNTER_CAPTCHA_KEY: Final = "dox_failure_counter_captcha_dj"

    def add_captcha(self, text: str, unique_id: str):
        """
        Добавляет каптчу в хранилище

        :param text: значение каптчи
        :param unique_id: уникальный идентификатор страницы
        """
        # Для отслеживания устаревших данных следует найти время жизни текста каптчи,
        # и добавить его вместе с текстом каптчи.
        redis.hset(self.DOX_CAPTCHA_KEY, unique_id, pickle.dumps(CaptchaRecord(text, self.get_captcha_lifetime())))

    def get_text(self, unique_id: str) -> str:
        """
        Возвращает текст каптчи

        :param unique_id: уникальный идентификатор страницы
        """
        return pickle.loads(redis.hget(self.DOX_CAPTCHA_KEY, unique_id)).text \
            if redis.hexists(self.DOX_CAPTCHA_KEY, unique_id) else None

    def get_captcha(self, unique_id: str) -> CaptchaRecord:
        """ Возвращает каптчу из хранилища по уникальному идентификатору запроса """
        return pickle.loads(redis.hget(self.DOX_CAPTCHA_KEY, unique_id)) if redis.hexists(self.DOX_CAPTCHA_KEY, unique_id) else None

    def remove_captcha(self, unique_id: str):
        """
        Удаляет каптчу из хранилища

        :param unique_id: уникальный идентификатор страницы
        """
        redis.hdel(self.DOX_CAPTCHA_KEY, unique_id)
        if redis.hexists(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id):
            redis.hdel(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id)

    def add_failure_validate(self, unique_id: str):
        """ Увеличивает количество неудачных попыток ввода каптч """
        # Если уже были неудачные попытки проверки каптчи,
        if redis.hexists(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id):
            # то берём структуру неудачных попыток,
            failure_counter_captcha_record: FailureCounterCaptchaRecord \
                = pickle.loads(redis.hget(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id))
            # и проверяем, если время жизни количества попыток уже истекло,
            if self.is_time_expired(failure_counter_captcha_record.elapsed_time):
                # то заново устанавливаем неудачную попытку проверки каптчи.
                self.add_failure_validate_captcha_attempt(unique_id)
            else:
                # А если ещё не истекло, то увеличиваем счётчик количества неудачных попыток.
                redis.hset(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id,
                           pickle.dumps(FailureCounterCaptchaRecord(
                               failure_counter_captcha_record.counter + 1, self.get_captcha_lifetime())))
        else:
            #  Если неудачных попыток ввода каптчи еще не было, то добавляю новую попытку.
            self.add_failure_validate_captcha_attempt(unique_id)

    def get_failure_validate_value(self, unique_id: str) -> int:
        """ Возвращает количество неудачных попыток ввода каптч """
        return pickle.loads(redis.hget(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id)).counter \
            if redis.hexists(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id) else 0

    def get_captcha_elapsed_time(self, unique_id: str) -> datetime:
        """ Возвращает время окончания действия каптчи """
        return pickle.loads(redis.hget(self.DOX_CAPTCHA_KEY, unique_id)).elapsed_time \
            if redis.hexists(self.DOX_CAPTCHA_KEY, unique_id) else None

    def get_captcha_counter_elapsed_time(self, unique_id: str) -> datetime:
        """ Возвращает время окончания действия счётчика неудачных попыток проверки каптчи """
        return pickle.loads(redis.hget(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id)).elapsed_time \
            if redis.hexists(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id) else None

    def remove_captcha_repository(self):
        """ Удаляет репозитории каптчи """
        if redis.hkeys(self.DOX_CAPTCHA_KEY):
            redis.delete(self.DOX_CAPTCHA_KEY)
        if redis.hkeys(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY):
            redis.delete(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY)

    def get_failure_counter_captcha(self, unique_id: str) -> FailureCounterCaptchaRecord:
        """ Возвращает неудачные попытки проверки катчи по уникальному идентификатору """
        return pickle.loads(redis.hget(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id)) \
            if redis.hexists(self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id) else None

    @classmethod
    def is_time_expired(cls, date_time: datetime) -> bool:
        """ Проверят просрочено ли время """
        return datetime.now() > date_time

    def add_failure_validate_captcha_attempt(self, unique_id: str):
        """
        Добавляет новую неудачную попытку проверки каптчи

        :param unique_id: уникальный идентификатор страницы
        """
        redis.hset(
            self.DOX_FAILURE_COUNTER_CAPTCHA_KEY, unique_id,
            pickle.dumps(FailureCounterCaptchaRecord(1, self.get_captcha_lifetime())))

    @classmethod
    def get_captcha_lifetime(cls) -> datetime:
        """ Возвращает время жизни каптчи """
        wait_reset_failed_validate: Final = getattr(settings, "WAIT_RESET_FAILED_VALIDATE", 30)
        # Вычисляем время жизни счётчика неудачных попыток каптчи.
        return datetime.now() + timedelta(minutes=wait_reset_failed_validate)
