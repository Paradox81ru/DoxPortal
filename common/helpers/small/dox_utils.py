from typing import Final

from django.urls import reverse
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.views import exception_handler
from rest_framework.request import HttpRequest

import hashlib



def reverse_params(view_name, args=None, kwargs=None, params=None, anchor=None):
    """
    Формирование строки URL с указанными параметрами

    :param view_name: наименование URL ссылки
    :param list, tuple args: список данных к ссылке
    :param dict kwargs: словарь именованных данных к ссылке
    :param dict params: именованные параметры идущее в ссылке после ?
    :param string anchor: якорная ссылка (переход по содержимому на сайте)
    :return:
    """
    params = params or dict()
    url = reverse(view_name, args=args, kwargs=kwargs)
    params = "&".join("{0}={1}".format(name, val) for name, val in params.items())
    params = f"?{params}" if params != "" else ""
    _anchor = f'#{anchor}' if anchor is not None else ''
    return url + params + _anchor


def get_choices_for_select_widget(choices, sort=None, is_empty_filter=False, name_empty_filter=None,
                                  value_empty_filter=None):
    """
    Формирует готовый список choices для элемента выбора select

    :param choices: список выбора
    :type choices: dict, list, tuple, set
    :param sort: тип сортировки (asc, desc)
    :param bool is_empty_filter: должен ли быть пустой фильтр
    :param str name_empty_filter: название пустого фильтра
    :param str value_empty_filter: значение пустого фильтра
    :return:
    """
    if isinstance(choices, dict):
        choices = _convert_dict_choices_to_list(choices)
    elif isinstance(choices, set):
        choices = list(zip(choices, choices))
    elif isinstance(choices, (list, tuple)) and not isinstance(choices[0], (list, tuple)):
        choices = list(zip(choices, choices))
    elif choices is None:
        # Иначе, если список не указан, то делаем список пустым списком.
        choices = []
    elif not isinstance(choices, (list, tuple)):
        raise TypeError("Неверный список выбора.")

    # Далее, если было указано, что список выбора должен быть отсортирован,
    if sort is not None and sort in ("asc", "desc"):
        # то создаём две вспомогательные функции для сортировки,
        def sort_list(item):
            # Если второй элемент списка является списком,
            if isinstance(item[1], (list, tuple)):
                # то этот список тоже надо отсортировать
                item[1] = sorted(item[1], key=sort_list)
            return item[0]

        # и сортировки в обратном порядке.
        def sort_list_reversed(item):
            # Если второй элемент списка является списком,
            if isinstance(item[1], (list, tuple)):
                # то этот список тоже надо отсортировать, но в обратном порядке.
                item[1] = sorted(item[1], key=sort_list, reverse=True)
            return item[0]

        # Если указали сортировку по возрастанию,
        if sort == "asc":
            # то произведём сортировку по возрастанию.
            choices = sorted(choices, key=sort_list)
        elif sort == "desc":
            # А если указали сортировку по убыванию, то отсортируем по убыванию.
            choices = sorted(choices, key=sort_list_reversed, reverse=True)

    # Если указано, что должен быть пустой фильтр,
    if is_empty_filter:
        # то добавим в начало списка пустой фильтр.
        choices.insert(0, (value_empty_filter, name_empty_filter))
    return choices


def _convert_dict_choices_to_list(choices):
    """
    Преобразует словарь выбора в пригодный для виджета select список выбора

    :param choices: словарь выбора
    :type choices: dict
    :return:
    """
    list_choices = []
    for key, item in choices.items():
        # Если значение тоже является словарем,
        if isinstance(item, dict):
            # то его тоже преобразуем в список.
            value = _convert_dict_choices_to_list(item)
        else:
            value = item
        list_choices.append((key, value))
    return list_choices


def get_request_ip(request: HttpRequest):
    """ Возвращает IP адрес клиента """
    ip_headers: Final = [
            "X-Forwarded-For",
            "Proxy-Client-IP",
            "WL-Proxy-Client-IP",
            "HTTP_X_FORWARDED_FOR",
            "HTTP_X_FORWARDED",
            "HTTP_X_CLUSTER_CLIENT_IP",
            "HTTP_CLIENT_IP",
            "HTTP_FORWARDED_FOR",
            "HTTP_FORWARDED",
            "HTTP_VIA",
            "REMOTE_ADDR"
    ]
    # you can add more matching headers here...
    for header in ip_headers:
        if header not in request.headers:
            continue
        value: str = request.headers.get(header)
        parts = value.split(",")
        return parts[0]
    return request.META.get("REMOTE_ADDR")


def get_unique_hash_page(request: HttpRequest) -> str:
    """ Возвращает уникальный HASH страницы (для страницы логина всегда будет 1) """
    url: str = request.headers.get("Referer") if "Referer" in request.headers else "unknown"
    if url.endswith("/login"):
        return '1'
    ip_address: str = get_request_ip(request)
    user_agent: str = request.headers.get("User-Agent") if "User-Agent" in request.headers else "unknown"
    combined_string = ip_address + user_agent + url
    return hashlib.md5(combined_string.encode('utf-8')).hexdigest()
