from zoneinfo import ZoneInfo

from django.utils import timezone, formats
import datetime


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