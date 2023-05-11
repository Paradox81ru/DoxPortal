from __future__ import annotations

from collections.abc import Sequence
import datetime
import zoneinfo
from typing import Final

import unicodedata
from django.urls import reverse
from django.utils.functional import classproperty
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str

from common.helpers.small import dox_utils, dox_lib
from common.helpers.small import dox_enumes

import enum


class UserRoles(enum.Enum):
    """ Перечисление ролей пользователей """
    system = 1
    super_admin = 2
    admin = 3
    admin_assistant = 4
    director = 5
    director_assistant = 6
    employee = 7
    visitor_vip = 8
    visitor = 9

    @classmethod
    def get_values(cls):
        """ Возвращает все значения перечисления """
        return (e.name for e in cls)

    @classmethod
    def get_items(cls):
        """ Возвращает пары номер - значение всех перечислений """
        return {e.value: e.name for e in cls}


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, role: str, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, password=password, **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        self._add_user_to_group(user)
        return user

    @classmethod
    def _add_user_to_group(cls, user):
        """
        Добавление пользователя в группу
        :param User user:
        :return:
        """
        # groups = {
        #     User.ROLE_SUPER_ADMIN: "superadmin",
        #     User.ROLE_SYSTEM: "system",
        #     User.ROLE_ADMIN: "admin",
        #     User.ROLE_ASSISTANT_ADMIN: "admin_assistant",
        #     User.ROLE_DIRECTOR: "director",
        #     User.ROLE_ASSISTANT_DIRECTOR: "director_assistant",
        #     User.ROLE_EMPLOYEE: "employee",
        #     User.ROLE_VIP_VISITOR: "visitor_vip"
        # }
        # Если указана роль пользователя и она присутствует в списке групп,
        if user.role is not None and user.role in UserRoles.get_values():
            # то найдем группу соответствующую роле пользователя,
            group = Group.objects.get(name=user.role)
            # и добавим пользователя в эту группу.
            user.groups.add(group)

    def create_user(self, username, email=None, password=None, role: str = None, **extra_fields):
        """
        Создает пользователя

        :param username: логин
        :param email: электронная почта
        :param password: пароль
        :param role: роль
        :param extra_fields:    is_staff - разрешен ли доступ пользователя к админке;
                                is_superuser - является ли пользователь суперпользователем;
                                status - статус пользователя (удален, заблокирован, активен);
                                role - роль пользователя (Админ, директор, посетитель, ...)
        :return:
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('status', User.STATUS_ACTIVE)
        return self._create_user(username, email, password, role, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """ Создает суперпользователя """
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('status', User.STATUS_ACTIVE)
        # extra_fields.setdefault('role', User.ROLE_SUPER_ADMIN)

        if extra_fields.setdefault('is_staff', True) is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.setdefault('is_superuser', True) is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        if extra_fields.setdefault('status', User.STATUS_ACTIVE) != User.STATUS_ACTIVE:
            raise ValueError('Суперпользователь должен быть активным.')
        # if extra_fields.setdefault('role', User.ROLE_SUPER_ADMIN) != User.ROLE_SUPER_ADMIN:
        #     raise ValueError('Суперпользователь должен быть суперпользователем.')

        return self._create_user(username, email, password, UserRoles.super_admin.name, **extra_fields)
        # group_admin = Group.objects.get(name='superadmin')
        # user.groups.add(group_admin)
        # return user

    def get_user(self, user):
        """
        Возвращает найденного пользователя по указанному идентификатору или имени пользователя.
        Если указали модель, то ее сразу и возвращают

        :param int, str, User user: пользователь которого надо вернуть. ID пользователя, username или модель User.
        :return:
        :rtype: User
        """
        # Если пользователь передан в виде модели,
        if isinstance(user, User):
            # то сразу ее и вернем.
            find_user = user
        elif isinstance(user, str):
            # Если передали логин пользователя, то найдем этого пользователя по логину.
            find_user = self.get(username__iexact=user)
        elif isinstance(user, int):
            # Так же найдем пользователя по его идентификатору (id)
            find_user = self.get(pk=user)
        else:
            raise TypeError(f"Поиск пользователя по идентификатору '{user}' невозможен.")
        # user.role = user.groups.name if user.groups is not None else UserRoles.visitor.name
        return find_user

    def check_unique_username(self, username):
        """
        Проверяет уникальность указанного логина:
        Вернет 1 - если такой логин уже существует в таблице пользователей;
        вернет 2 - если такой логин уже существует в таблице временных пользователей;
        вернет 0 - если этот логин уникален.

        :param str username: логин
        """
        # Если в таблице пользователей такой пользователь уже существует, то вернем 1.
        if len(self.filter(username=username)) != 0:
            return 1
        # Иначе если в таблице временных пользователей такой пользователь уже существует, то вернем 2.
        elif len(TempUser.objects.filter(username=username)) != 0:
            return 2
        # Иначе вернем 0
        return 0

    def check_unique_email(self, email):
        """
        Проверяет уникальность указанного email.
        Вернет 1 - если такой email уже существует в таблице пользователей;
        вернет 2 - если такой email уже существует в таблице временных пользователей;
        вернет 0 - если этот email уникален.
        """
        # Если в таблице пользователей такой email уже существует,
        if len(self.filter(email=email)) != 0:
            # то вернем 1.
            return 1
        # Иначе если в таблице временных пользователей такой email уже существует,
        elif len(TempUser.objects.filter(email=email)) != 0:
            # то вернем 2.
            return 2
        # Иначе вернем 0
        return 0


class User(AbstractUser):
    """ Моя модель пользователей """
    STATUS_DELETED: Final = 1  # Удален
    STATUS_BLOCKED: Final = 2  # Заблокирован
    STATUS_ACTIVE: Final = 10  # Активен
    LIST_STATUSES: Final = {
        STATUS_DELETED: "удален",
        STATUS_BLOCKED: "заблокирован",
        STATUS_ACTIVE: "активен"
    }

    @classproperty
    def field_meta_data(self):
        return [
            FormFieldMetaData("username", "id_username", "Логин", dox_enumes.TYPE_TEXT, True,
                              {"maxLength": "100", "minLength": "3"},
                              ("Логин должен быть правильным", "Логин не должен быть пустым", "Логин не должен повторяться")),
            FormFieldMetaData("password", "id_password", "Пароль", dox_enumes.TYPE_PASSWORD, True),
            FormFieldMetaData("verifyCaptcha", "idVerifyCaptcha", "Введите код с картинки", dox_enumes.TYPE_TEXT, True,
                              {"autoComplete": "off"}),
            FormFieldMetaData("rememberMe", "idRememberMe", "Запомнить", dox_enumes.TYPE_CHECKBOX, False)
        ]

    # ROLE_SUPER_ADMIN: Final = 1            # Суперадмин
    # ROLE_SYSTEM: Final = 2                 # Система
    # ROLE_ADMIN: Final = 10                 # Aдмин
    # ROLE_ASSISTANT_ADMIN: Final = 11       # Помощник админа
    # ROLE_DIRECTOR: Final = 20              # Директор
    # ROLE_ASSISTANT_DIRECTOR: Final = 21    # Помощник директора
    # ROLE_EMPLOYEE: Final = 30              # Сотрудник
    # ROLE_VIP_VISITOR: Final = 40           # Особый посетитель
    # ROLE_VISITOR: Final = 41               # Посетитель
    # LIST_ROLES: Final = {
    #     ROLE_SUPER_ADMIN: "суперадмин",
    #     ROLE_SYSTEM: "система",
    #     ROLE_ADMIN: "админ",
    #     ROLE_ASSISTANT_ADMIN: "помощник админа",
    #     ROLE_DIRECTOR: "директор",
    #     ROLE_ASSISTANT_DIRECTOR: "помощник директора",
    #     ROLE_EMPLOYEE: "сотрудник",
    #     ROLE_VIP_VISITOR: "особый посетитель",
    #     ROLE_VISITOR: "посетитель"
    # }

    CAN_ADD_SOFTWARE = "accounts.add_software"
    CAN_BLOCKING_SOFTWARE = "accounts.blocking_software"
    CAN_REMOVE_OTHER_SOFTWARE = "accounts.remove_other_software"
    CAN_BLOCKING_ARTICLES = "accounts.blocking_articles"
    CAN_DELETE_NOTIFY = "accounts.delete_message_notify"
    CAN_ADMIN_TINYMCE = "accounts.admin_tinymce"
    CAN_SEND_UNSAFE_PERSONAL_MESSAGE = "accounts.send_unsafe_personal_message"
    EDIT_OTHER_COMMENTS = "accounts.edit_other_comments"
    # Группы разрешенных количества тэгов в статье
    UNLIMITED_COUNT_TAGS = "accounts.unlimited_count_tags"
    BIG_COUNT_TAGS = "accounts.big_count_tags"
    MEDIUM_COUNT_TAGS = "accounts.medium_count_tags"
    SMALL_COUNT_TAGS = "accounts.small_count_tags"
    DEFAULT_COUNT_TAGS = "accounts.default_count_tags"

    COUNT_TAGS = {
        UNLIMITED_COUNT_TAGS: 30,     # неограниченое количество тэгов
        BIG_COUNT_TAGS: 10,         # большое количество тэгов
        MEDIUM_COUNT_TAGS: 5,       # среднее количество тэгов
        SMALL_COUNT_TAGS: 3,        # малое количество тэгов
        DEFAULT_COUNT_TAGS: 3,      # количество тэгов по умолчанию
        }

    email = models.EmailField('Электронная почта', unique=True)
    # role = models.IntegerField("Роль", choices=dox_utils.get_choices_for_select_widget(LIST_ROLES),
    #                            default=ROLE_VISITOR)
    status = models.IntegerField("Статус", choices=dox_utils.get_choices_for_select_widget(LIST_STATUSES), default=10)
    ip_address = models.CharField("IP адрес", max_length=40, blank=True, null=True)
    time_zone = models.CharField("Временная зона",
                                 choices=dox_utils.get_choices_for_select_widget(
                                     sorted(zoneinfo.available_timezones())), max_length=32,
                                 default='Europe/Moscow')

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']
        permissions = [
            ("add_software", "Может добавлять приложения"),
            ("blocking_software", "Может блокировать приложения"),
            ("remove_other_software", "Может удалять чужие приложения"),
            ("blocking_articles", "Может блокировать статьи"),
            ("delete_message_notify", "Может удалять уведомления"),
            ("admin_tinymce", "Редактор tinymce для администратора"),
            ("send_unsafe_personal_message", "Отправлять небезопасные персональные сообшения"),
            ("edit_other_comments", "Редактировать или удалять чужие комментарии"),
            ("default_count_tags", "Количество тэгов по умолчанию"),
            ("small_count_tags", "Малое количество тэгов"),
            ("medium_count_tags", "Среднее количество тэгов"),
            ("big_count_tags", "Большое количество тэгов"),
            ("unlimited_count_tags", "Неограниченное количество тэгов")
        ]

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, val: str):
        self._role = val

    def create_temp_user_from_request_password_reset(self):
        """ Создает временного пользователя при запросе на сброс пароля """
        # Для начала сформирую новый токен.
        token = get_random_string(24)
        try:
            # Далее пробую найти, есть ли уже временный пользователь.
            temp_user = TempUser.objects.get(username=self.username, process=TempUser.PROCESS_RESET_PASSWORD)
            # Если есть,
            if temp_user.is_actual:
                # то сразу его и верну.
                return temp_user
            # Иначе удаляю этого временного пользователя.
            temp_user.delete()
        except TempUser.DoesNotExist:
            pass

        # Создаю нового временного пользователя.
        temp_user = TempUser(token=token,
                             role=self.groups,
                             username=self.username,
                             email=self.email,
                             process=TempUser.PROCESS_RESET_PASSWORD
                             )
        # noinspection PyBroadException
        try:
            # Далее пробю сохранить временного пользователя,
            temp_user.save()
            # и возвращаю его.
            return temp_user
        except Exception:
            return None

    def change_data(self, data):
        """
        Изменяет значения данных пользователя

        :param dict data: словарь данных в соответствии с которым надо произвести изменения данных.
        :return:
        """
        # Чтобы не изменить id, который менять нельзя,
        if "id" in data:
            # удаляю его сразу из данных на изменения.
            del (data["id"])
            # Дальше проверяю, если логин изменяется,
        if data["username"] != self.username:
            # и предлагаемый логин уже существует, или ждет подтверждения,
            if User.objects.check_unique_username(data["username"]) != 0:
                # то вызываю исключение.
                raise self.NotUniqueUsername
        # Иначе прохожу по всем предлагаемым изменениям,
        for item in data:
            # и если предлагаемое изменение можно произвести,
            if hasattr(self, item):
                # то изменяю соответсвующий атрибут на предлагаемое изменение.
                setattr(self, item, data[item])
        # Сохраняю изменения в базу данных
        self.save()

    def get_full_name(self):
        """ Возвращает имя и фамилию, если они указаны, а если не указаны, то логин """
        full_name = super().get_full_name().strip()
        return self.username if len(full_name) == 0 else full_name

    # def get_unread_personal_messages(self):
    #     """ Возвращает все непрочитанные персональные сообщения текущего пользователя """
    #     # pattern = f'(,|^){self.id}(,|$)'
    #     # Получим шаблон для проверки уведомления на прочитанность по регулярному выражению.
    #     pattern = PersonalMessage.get_pattern(self)
    #     # Вернем только непрочитанные и не удаленные уведомления, и сообщения (is_ready=False).
    #     # Если уведомление непрочитано, то по следующему шаблону в строке списке пользователей прочитавших уведомление,
    #     # ничего найдено не будет.
    #     return PersonalMessage.objects.filter(
    #         (((Q(message_type=PersonalMessage.TYPE_NOTIFY) | Q(message_type=PersonalMessage.TYPE_SYSTEM_NOTIFY)) & Q(
    #             is_delete=False)) &
    #          ~Q(notify_ready__regex=pattern)) | (Q(to_user=self.id) & ~Q(is_ready=True)))

    # def get_all_personal_messages(self):
    #     """ Возвращает все персональные сообщения текущего пользователя и общие уведомления """
    #     return PersonalMessage.objects.filter(Q(to_user=self.id) |
    #                                           ((Q(message_type=PersonalMessage.TYPE_NOTIFY) | Q(
    #                                               message_type=PersonalMessage.TYPE_SYSTEM_NOTIFY)) & Q(
    #                                               is_delete=False)))

    @property
    def is_admin(self):
        """ Является ли пользователь администратором """
        return self.is_superuser

    def is_included_in_any_group(self, groups):
        """
        Проверяет, включен ли пользователь в любую из указанных групп

        :param iter, str groups: группа или список групп для проверки.
        :return:
        """
        # Для начала, если передали группу в виде одной группы,
        if isinstance(groups, str):
            # то преобразуем ее в список.
            groups = [groups]
        # Далее вытащим список групп, к которым принадлежит пользователь.
        incl_groups = list(self.groups.values_list('name', flat=True))

        # Пройдемся по списку переданных групп,
        for group in groups:
            # и проверим, если эта группа входит в список групп, к которым пользователь принадлежит,
            if group in incl_groups:
                # то вернем True
                return True
        # Если ни одной группе пользователь не принадлежит, то вернем False
        return False

    def is_included_in_all_groups(self, groups):
        """
        Проверяет, включен ли пользователь во все из указанные группы

        :param iter, str groups: группа или список групп для проверки.
        :return:
        """
        # Для начала, если передали группу в виде одной группы,
        if isinstance(groups, str):
            # то преобразуем ее в список.
            groups = [groups]
        # Далее вытащим список групп, к которым принадлежит пользователь.
        incl_groups = list(self.groups.values_list('name', flat=True))
        # Пройдемся по списку переданных групп,
        for group in groups:
            # и проверим, если эта группа не входит в список групп, к которым пользователь принадлежит,
            if group not in incl_groups:
                # то сразу вернем False
                return False
        # Если пользователь принадлежит всем указанным группам, то вернем True
        return True

    # @property
    # def get_number_of_tags_allowed(self):
    #     """ Возвращает количество разрешенных тегов в статье для текущего пользователя """
    #     # Пробежимся по словарю разрешений,
    #     for perm, count_tags in self.COUNT_TAGS.items():
    #         # и если пользователь имеет разрешение,
    #         if self.has_perm(perm):
    #             # то вернем количество разрешенных тэгов для данного разрешения
    #             return count_tags
    #     # Если нужного разрешения нет, то вернем количество тэгов по умолчанию.
    #     return self.COUNT_TAGS.get(self.DEFAULT_COUNT_TAGS)

    class NotUniqueUsername(Exception):
        pass


class TempUserManager(models.Manager):
    # class Meta:
    #     verbose_name = "Пользователь"
    #     verbose_name_plural = "Пользователи"
    #     ordering = ['username']

    def create_temp_user(self, username, email, password, request, role=None):
        """ Создает временного пользователя """
        role = role or UserRoles.visitor.value
        token = get_random_string(24)
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[-1].strip()
        time_zone = self._get_timezone(ip_address)
        temp_user = TempUser(token=token,
                             role=role,
                             username=self.model.normalize_username(username),
                             email=dox_lib.normalize_email(email),
                             password=make_password(password),
                             process=TempUser.PROCESS_CONFIRM_ACCOUNT,
                             ip_address=ip_address,
                             time_zone=time_zone
                             )
        # noinspection PyBroadException
        try:
            temp_user.save()
            return temp_user
        except Exception:
            return None

    # @classmethod
    # def request_confirm_account(cls, request, temp_user):
    #     return cls._send_email(request, temp_user, 'email_confirm_account.html', 'confirm-account')
    #
    # @classmethod
    # def request_new_password(cls, request, token):
    #     # Для начала попробуем найти временного пользователя по указанному токену.
    #     temp_user = TempUser.objects.get(token=token)
    #     return cls._send_email(request, temp_user, 'email_request_new_password.html', 'confirm-reset-password')

    # @classmethod
    # def _send_email(cls, request, temp_user, template_name, site_name, ext_context=None):
    #     """ Отправляет письмо по электронной почте """
    #     subject = 'Сообщение с сайта "Парадокс-портал".'
    #     url = request.get_host() + reverse(f'accounts:{site_name}', args=[temp_user.token])
    #     context = {'username': temp_user.username, 'link': url}
    #     if ext_context is not None:
    #         context.update(ext_context)
    #     return dox_utils.send_email_template(subject, temp_user.email, f'accounts/email/{template_name}', context, request)

    # @staticmethod
    # def _get_timezone(ip_address):
    #     geoip_base_dir = settings.BASE_GEOIP_FILES_DIR
    #     geoip = DoxGeoIp(geoip_base_dir, 'ru')
    #     # noinspection PyBroadException
    #     try:
    #         time_zone = geoip.get_timezone(ip_address)
    #     except Exception:
    #         time_zone = settings.TIME_ZONE
    #     return time_zone


class TempUser(models.Model):
    """ Временные пользователи требующие подтверждения аккаунта """
    # Количество дней, после котрого временный пользователь будет считаться просроченным.
    NUMBER_DAYS_TO_DELAY = 15

    PROCESS_CONFIRM_ACCOUNT = 1
    PROCESS_RESET_PASSWORD = 2
    PROCESS_CHANGED_EMAIL = 3

    LIST_PROCESS = {
        PROCESS_CONFIRM_ACCOUNT: "подтверждение аккаунта",
        PROCESS_RESET_PASSWORD: "сброс пароля",
        PROCESS_CHANGED_EMAIL: "смена email"
    }

    choices_role = dox_utils.get_choices_for_select_widget(UserRoles.get_items())
    choices_process = dox_utils.get_choices_for_select_widget(LIST_PROCESS)

    token = models.CharField("Токен", primary_key=True, max_length=24)
    #    role = models.IntegerField("Роль", blank=True, null=True, choices=((0, None),) + User.LIST_ROLES_1)
    role = models.IntegerField("Роль", choices=choices_role, default=UserRoles.visitor.value)
    username = models.CharField("Логин", max_length=150, unique=True)
    password = models.CharField('Пароль', blank=True, null=True, max_length=128)
    email = models.EmailField('Электронная почта', blank=True, null=True, db_index=True)
    date_joined = models.DateTimeField('Дата запроса', default=timezone.now)
    ip_address = models.CharField("IP адрес", max_length=40, blank=True, null=True)
    time_zone = models.CharField("Временная зона",
                                 choices=dox_utils.get_choices_for_select_widget(
                                     sorted(zoneinfo.available_timezones())), max_length=32,
                                 default='Europe/Moscow')
    #    process = models.IntegerField("Процедура", choices=LIST_PROCESS_1, default=PROCESS_CONFIRM_ACCOUNT)
    process = models.IntegerField("Процедура", choices=choices_process, default=PROCESS_CONFIRM_ACCOUNT)

    objects = TempUserManager()

    class Meta:
        verbose_name = "Временный пользователь"
        verbose_name_plural = "Временные пользователи"

    def import_temp_user_to_user(self):
        """ Создает нового пользователя и текущего временного пользователя """
        user = User(username=self.username, email=self.email, password=self.password, role=self.role,
                    ip_address=self.ip_address, time_zone=self.time_zone)
        user.save()
        # User.objects.create_user(self.username, self.email, self.password, role=self.role,
        #                          ip_address=self.ip_address, time_zone=self.time_zone)

    def update_temp_user(self, data):
        """
        Обновляет переданные данные временного пользователя, но не сохраняет их.

        :param dict data: данные в виде словаря
        :return:
        """

        for attr, val in data.items():
            setattr(self, attr, val)

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', force_str(username))

    # def repeated_request_confirm_account(self, request):
    #     """ Повторный запрос на подтверждение аккаунта """
    #     return self._send_email(request, 'email_confirm_account.html', 'confirm-account') != 0
    #
    # def repeated_request_reset_password(self, request):
    #     """ Повторный запрос на сброс пароля """
    #     return self._send_email(request, 'email_request_new_password.html', 'confirm-reset-password') != 0

    @property
    def is_actual(self):
        """ Не просрочен ли временный пользователь """
        data_now = datetime.datetime.now().date()
        return (data_now - self.date_joined.date()).days < TempUser.NUMBER_DAYS_TO_DELAY

    @classmethod
    def request_confirm_account(cls, request, temp_user):
        return cls._send_email(request, temp_user, 'email_confirm_account.html', 'confirm-account')

    @classmethod
    def request_new_password(cls, request, token):
        # Для начала попробуем найти временного пользователя по указанному токену.
        temp_user = TempUser.objects.get(token=token)
        return cls._send_email(request, temp_user, 'email_request_new_password.html', 'confirm-reset-password')

    @classmethod
    def _send_email(cls, request, temp_user, template_name, site_name, ext_context=None):
        """ Отправляет письмо по электронной почте """
        subject = 'Сообщение с сайта "Парадокс-портал".'
        url = request.get_host() + reverse(f'accounts:{site_name}', args=[temp_user.token])
        context = {'username': temp_user.username, 'link': url}
        if ext_context is not None:
            context.update(ext_context)
        return dox_utils.send_email_template(subject, temp_user.email, f'accounts/email/{template_name}', context, request)

    def __str__(self):
        return f'{self.username} {self.LIST_PROCESS[self.process]}'


class FormFieldMetaData:
    """
    Класс записи для формирования данных о поле формы
    """

    def __init__(self, field_name: str, _id: str, label: str, field_type: str, is_required: bool,
                 input_attributes: dict[str, str] = None, helper: Sequence[str] = None, value_list: Sequence[set] = None):
        """
        Конструктор класса записей для формирования данных о поле формы

        :param field_name: имя поля;
        :param _id: уникальный идентификатор поля;
        :param label: метка поля
        :param field_type: тип поля
        :param is_required: обязательное ли поле
        :param input_attributes: дополнительные аттрибуты для поля ввода
        :param helper: список подсказок для правильного внесения данных в поле
        :param value_list: проверяется ли поле на корректность ввода
        """

        self.fieldName: str = field_name
        self.id: str = _id
        self.label: str = label
        self.fieldType: str = field_type
        self.isRequired: bool = is_required
        self.inputAttributes: dict[str, str] = input_attributes
        self.helper: Sequence[str] = helper
        self.valueList: Sequence[set] = value_list
