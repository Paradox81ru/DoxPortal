from zoneinfo import ZoneInfo

from django.core.cache import caches
from django.utils import timezone, formats
import datetime

from main.models import Paradox

import random


class HeaderParadox:
    @classmethod
    def rnd_paradox(cls):
        cache = caches['redisCache']
        # Попробуем получить парадокс из кэша.
        text_paradox = cache.get('text_paradox')
        # Если в кэше пардокса нет,
        if text_paradox is None:
            # то найдем все доступные парадоксы (вернее их id) (которые активны, и которые еще не выбирались).
            paradoxes_id = list(Paradox.objects.get_can_choices_paradox_id())
            # Если выбрано парадоксов не было, то проверим,
            if len(paradoxes_id) == 0:
                # а есть ли вообще парадоксы в базе данных?
                if Paradox.objects.count() == 0:
                    # Если нет, то парадокс будет пустым.
                    return {'header': '', 'content': ''}
                else:
                    # Иначе изменим у всех парадоксов флаг выбираемости на True,
                    Paradox.objects.set_all_can_choices_paradox()
                    # и снова выберим все доступные парадоксы.
                    paradoxes_id = list(Paradox.objects.get_can_choices_paradox_id())
            # Среди списка идентификаторов доступных парадоксов выберим один случайный,
            paradox_id = random.choice(paradoxes_id)
            # и теперь уже вытащим парадокс с выбранным идентификатором.
            paradox = Paradox.objects.get(id=paradox_id)
            # Отключим у этого парадокса флаг выбираемости, чтобы он пока не учавствовал в выборе,
            paradox.is_choices = False
            # и сохраним этот парадокс.
            paradox.save(update_fields=['is_choices'])
            # Подготовим текст парадокса,
            text_paradox = {'header': paradox.header, 'content': paradox.content}
            # и сохраним текст парадокса в кэше, на срок до указанного вермени
            cache.set('text_paradox', text_paradox, cls._get_timeout_cache('00:00').seconds)
        # Вернем текст парадокса.
        return text_paradox

    @classmethod
    def _get_timeout_cache(cls, str_timeout):
        """ Возвращает время истекания актуальности кэша """
        # Получим текущую дату.
        date_now = datetime.datetime.now()
        # Преобразуем указанное время истекания актуальности кэша.
        timeout = cls._parse_time(date_now, str_timeout)
        # Если это время раньше текущего времени,
        if date_now > timeout:
            # то сложим два периода, первый разницу между почти полночью (за минуту до) и текущем временем
            # и второй период это разница между истекающим временем и полночью.
            time_delta = (cls._parse_time(date_now, "23:59") - date_now) + (
                    timeout - cls._parse_time(date_now, "00:00"))
        else:
            # Если же это время позже, то тогда просто вычмти из истекающего времени текущее время.
            time_delta = timeout - date_now
        return time_delta

    @classmethod
    def _parse_time(cls, date_now: datetime, s: str) -> datetime:
        """ Преобразует указанное строковое время (часы:минуты) в формат datetime """
        # Разобьем указанное время по двоеточию,
        hour, minute, = s.split(':')
        # и далее создадим датувремя с указанной сегодняшней датой, но преобразованным из указанной строки времени.
        return datetime.datetime(date_now.year, date_now.month, date_now.day, int(hour), int(minute))


def format_date(value, arg=None, tz=None, is_localtime=None):
    """
    Форматирование даты-времени

    :param value: дата-время
    :param arg: дополнительные аргументы
    :param tz: временная зона в которой надо вывести время
    :param is_localtime: вывести в локальном времени
    :return:
    """
    if value in (None, ''):
        return ''
    if isinstance(value, datetime.datetime):
        if tz is not None:
            set_timezone = ZoneInfo(tz)
            try:
                value = set_timezone.localize(value)
            except ValueError:
                value = value.astimezone(set_timezone)
        elif is_localtime is not None and is_localtime:
            value = timezone.localtime(value)

    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''