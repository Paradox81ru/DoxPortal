from typing import Final
from collections.abc import Sequence

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.cache import caches

from dataclasses import dataclass

import random
import datetime

from accounts.models import User
from my_admin.models import Permission

DEFAULT: Final = "default"
PRIMARY: Final = "primary"
SECONDARY: Final = "secondary"
SUCCESS: Final = "success"
DANGER: Final = "danger"
WARNING: Final = "warning"
INFO: Final = "info"
LIGHT: Final = "light"
DARK: Final = "dark"
LINK: Final = "link"


class ParadoxManager(models.Manager):
    def get_can_choices_paradox_id(self):
        """ Возвращает только те id парадоксов, которые пригодны для выбора """
        return self.model.objects.filter(is_enabled=True, is_choices=True).values_list('id', flat=True)

    def set_all_can_choices_paradox(self):
        """ Устанавливает все парадоксы разрешенными для выбора """
        self.model.objects.all().update(is_choices=True)

    @property
    def rnd_paradox(self):
        """ Возвращает случайный парадокс """
        cache = caches['redisCache']
        # Попробуем получить парадокс из кэша.
        text_paradox = cache.get('text_paradox')
        # Если в кэше пардокса нет,
        if text_paradox is None:
            # то найдем все доступные парадоксы (вернее их id) (которые активны, и которые еще не выбирались).
            paradoxes_id = list(self.get_can_choices_paradox_id())
            # Если выбрано парадоксов не было, то проверим,
            if len(paradoxes_id) == 0:
                # а есть ли вообще парадоксы в базе данных?
                if self.model.objects.all().count() == 0:
                    # Если нет, то парадокс будет пустым.
                    return {'header': '', 'content': ''}
                else:
                    # Иначе изменим у всех парадоксов флаг выбираемости на True,
                    self.set_all_can_choices_paradox()
                    # и снова выберим все доступные парадоксы.
                    paradoxes_id = list(self.get_can_choices_paradox_id())
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
            cache.set('text_paradox', text_paradox, self._get_timeout_cache('00:00').seconds)
        # Вернем текст парадокса.
        return text_paradox

    def _get_timeout_cache(self, str_timeout):
        """ Возвращает время истекания актуальности кэша """
        # Получим текущую дату.
        date_now = datetime.datetime.now()
        # Преобразуем указанное время истекания актуальности кэша.
        timeout = self._parse_time(date_now, str_timeout)
        # Если это время раньше текущего времени,
        if date_now > timeout:
            # то сложим два периода, первый разницу между почти полночью (за минуту до) и текущем временем
            # и второй период это разница между истекающим временем и полночью.
            time_delta = (self._parse_time(date_now, "23:59") - date_now) + (
                    timeout - self._parse_time(date_now, "00:00"))
        else:
            # Если же это время позже, то тогда просто вычтем из истекающего времени текущее время.
            time_delta = timeout - date_now
        return time_delta

    @classmethod
    def _parse_time(cls, date_now: datetime, s: str) -> datetime:
        """ Преобразует указанное строковое время (часы:минуты) в формат datetime """
        # Разобьем указанное время по двоеточию,
        hour, minute, = s.split(':')
        # и далее создадим дату-время с указанной сегодняшней датой, но преобразованным из указанной строки времени.
        return datetime.datetime(date_now.year, date_now.month, date_now.day, int(hour), int(minute))


class Paradox(models.Model):
    header = models.CharField("Заголовок", max_length=255, db_index=True)
    content = models.TextField("Парадокс")
    is_choices = models.BooleanField("Участвует в выборе", default=True)
    is_enabled = models.BooleanField("Парадокс активен", default=True)

    class Meta:
        app_label = "main"
        verbose_name = "Парадокс"
        verbose_name_plural = "Парадоксы"

    def change_data(self, data):
        """ Изменяет значение данных парадокса """
        # Далее пробежимся по всем предлагаемым изменениям,
        for item in data:
            # Если передано id,
            if item == 'id':
                # то пропустим его и перейдем к следующему атрибуту
                continue
            # и если предлагаемое изменение можно произвести,
            if hasattr(self, item):
                # то изменим соответсвующий атрибут на предлагаемое изменение.
                setattr(self, item, data[item])
        # Сохраним изменения в базу данных
        self.save()

    objects = ParadoxManager()

    def __str__(self):
        return f'{self.header}'


def get_breadcrumb_list():
    """ Возвращает список хлебных крошек """
    breadcrumb_list = {"": (("Главная",),)}
    main = ("Главная", "/")
    breadcrumb_list["/login"] = (main, ("Вход",))
    breadcrumb_list["/about"] = (main, ("О сайте",))
    breadcrumb_list["/copyright"] = (main, ("Права на сайт",))
    breadcrumb_list["/contact"] = (main, ("Обратная связь",))
    return breadcrumb_list


def get_admin_breadcrumb_list():
    """ Возвращает список хлебных крошек для Админки """
    breadcrumb_list = {"/dox-admin": (("Главная",),)}
    main = ("Главная", "/dox-admin")
    breadcrumb_list["/dox-admin/edit-profile"] = (main, ("Редактирование профилей",))
    breadcrumb_list["/dox-admin/manage-temp-user"] = (main, ("Редактирование временных пользователей",))
    return breadcrumb_list


@dataclass
class MainMenu:
    label: str
    style: str
    icon: str
    url: str
    is_real: bool
    items: Sequence["MainSubmenu"]


@dataclass
class MainSubmenu:
    label: str
    url: str


def get_main_menu_list(user: User):
    is_auth = user.is_authenticated
    is_can_see_menu_admin = is_auth and user.has_perm(Permission.can_see_menu_admin)
    is_can_add_software = is_auth and user.has_perm(User.CAN_ADD_SOFTWARE)
    is_admin = is_auth and user.is_admin

    main_manu_list = []
    # Меню "Админка" должно быть видно только пользователям с привилегией видеть меню администратора.
    if is_can_see_menu_admin:
        main_manu_list.append(MainMenu("Админка", DANGER, "gears", "/dox-admin", True, []))

    # Меню "Профиль" и "Блогер" должно быть видно только авторизованным пользователям.
    if is_auth:
        main_manu_list.append(MainMenu("Профиль", INFO, "id-badge", "#", False, (
            MainSubmenu("Изменить пароль", "/account/password-change"),
            MainSubmenu("Изменить профиль", f"/account/edit-profile/{user.id}"))))
        main_manu_list.append(MainMenu("Блогер", INFO, "pen-to-square", "#", False, (
            MainSubmenu("Добавить статью", "#"),
            MainSubmenu("Свои статьи", "#"),
            MainSubmenu("Заблокированные статьи", "#")
        )))

    if is_auth and is_can_add_software:
        submenu_list = [
            MainSubmenu("Добавить приложение", "#"),
            MainSubmenu("Свои приложения", "#"),
            MainSubmenu("Заблокированные приложения", "#")
        ]
        if is_admin:
            submenu_list.append(MainSubmenu("Добавить сервис", "#"))
            submenu_list.append(MainSubmenu("Список сервисов", "#"))
        main_manu_list.append(MainMenu("Программист", INFO, "code", "#", False, submenu_list))

    if is_can_see_menu_admin:
        main_manu_list.append(MainMenu("Галерист", INFO, "paintbrush", "#", False, (
            MainSubmenu("Добавить раздел", "#"),
            MainSubmenu("Список разделов", "#"),
            MainSubmenu("Добавить изображение", "#"),
            MainSubmenu("Список изображений", "#")
        )))

    main_manu_list.append(MainMenu("Статьи", DEFAULT, "pencil", "/blog/articles", False, []))
    main_manu_list.append(MainMenu("Приложения", DEFAULT, "file-code", "#", False,(
        MainSubmenu("Скачать", "/software/downloads"),
        MainSubmenu("Зарегистрировать", "/software/get-register-number"))))
    main_manu_list.append(MainMenu("Сервисы", DEFAULT, "wrench", "/service", False, []))
    main_manu_list.append(MainMenu("Фото-фэнтези", DEFAULT, "dragon", "/picture", False, []))
    return main_manu_list


def get_main_menu():
    return MainMenu("Приложения", DEFAULT, "file-code", "#", False,
                                   (MainSubmenu("Скачать", "/software/downloads"),
                                    MainSubmenu("Зарегистрировать", "/software/get-register-number")))