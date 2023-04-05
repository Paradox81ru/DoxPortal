import random

from django.core.management import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from django.utils import timezone

# from accounts.models import User, TempUser, PersonalMessage
# from blog.models import Article
from accounts.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-ca', '--count_articles', type=int, nargs='?', help="Number of added articles")
        parser.add_argument('-cu', '--count_users', type=int, nargs='?', help="Number of added users")
        parser.add_argument('-ctu', '--count_temp_users', type=int, nargs='?', help="Number of added temp users")
        parser.add_argument('-cps', '--count_personal_message', type=int, nargs='?', help="Number of personal messages")

    def handle(self, *args, **options):
        count_articles = options.get("count_articles", None)
        count_users = options.get("count_users", None)
        count_temp_users = options.get("count_temp_users", None)
        count_personal_message = options.get("count_personal_message", None)

        if count_articles is not None and count_articles > 0:
            self._add_random_articles(count_articles)
        if count_users is not None and count_users > 0:
            self._add_random_users(count_users)
        if count_temp_users is not None and count_temp_users > 0:
            self._add_random_temp_users(count_temp_users)
        if count_personal_message is not None and count_personal_message > 0:
            self._add_random_personal_messages(count_personal_message)

    # def _add_random_articles(self, count):
    #     # Для начала получим идентификаторы всех пользователей.
    #     list_users_id = tuple(User.objects.raw("SELECT id FROM accounts_user"))
    #     count_articles = Article.objects.count()
    #     # Далее надо создать указанное количество раз статьи, и сохранить их.
    #     for i in range(1, count + 1):
    #         num = count_articles + i
    #         # Возьмем случайны идентификатор пользователя,
    #         user_id = random.choice(list_users_id)
    #         # и назначим его новой статье.
    #         author = user_id
    #         header = f'Статья №{num}'
    #         # if article.status == Article.STATUS_PUBLISHED:
    #         #     article.published_at = timezone.now()
    #         description = f'Описание статьи №{num}'
    #         content = f'Какое-то содержимое {num}'
    #         status = random.choice(Article.LIST_STATUSES)
    #         extra_fields = dict()
    #         # Если указан статус заблокированно,
    #         if status == Article.STATUS_BLOCKED:
    #             # то нужно указать причину блокировки.
    #             extra_fields['reason_blocking'] = f"Причина блокировки {header}"
    #
    #         # Создадим новую статью.
    #         article = Article.objects.create_article(author, header, description, content, status, **extra_fields)
    #         article.save()
    #     self.stdout.write(f"Добавлено {count} случайных статей.")

    def _add_random_users(self, count):
        count_user = User.objects.count()
        for i in range(1, count + 1):
            user = User()
            num = count_user + i
            user.username = f"User_{num}"
            user.email = f"email.user{num}@mail.local"
            user.set_password(user.username)
            user.ip_address = '195.177.105.122'
            user.role = User.ROLE_VISITOR
            user.status = User.STATUS_ACTIVE
            user.save()
        self.stdout.write(f"Добавлено {count} случайных пользователей.")

    # def _add_random_temp_users(self, count):
    #     count_temp_user = TempUser.objects.count()
    #     for i in range(1, count + 1):
    #         temp_user = TempUser()
    #         num = count_temp_user + i
    #         temp_user.token = get_random_string(24)
    #         temp_user.username = f"Temp_user_{num}"
    #         temp_user.email = f"email.temp_user{num}@mail.local"
    #         temp_user.password = make_password(temp_user.username)
    #         temp_user.ip_address = '195.177.105.122'
    #         temp_user.role = User.ROLE_VISITOR
    #         temp_user.process = TempUser.PROCESS_CONFIRM_ACCOUNT
    #         temp_user.save()
    #     self.stdout.write(f"Добавлено {count} случайных временных пользователей.")

    # def _add_random_personal_messages(self, count):
    #     message_count = PersonalMessage.objects.count()
    #     list_func = list()
    #     list_func.append(lambda j: PersonalMessage.objects.send_personal_message('Admin', 'Paradox', f'Личное сообщение №{j}', False))
    #     list_func.append(lambda j: PersonalMessage.objects.send_personal_message('Paradox', 'Admin', f'Личное сообщение №{j}', False))
    #     list_func.append(lambda j: PersonalMessage.objects.send_system_message('Admin', f'Системное сообщение №{j}', False))
    #     list_func.append(lambda j: PersonalMessage.objects.send_system_message('Paradox', f'Системное сообщение №{j}', False))
    #     list_func.append(lambda j: PersonalMessage.objects.send_notify_system(f'Уведомление №{j}', False))
    #
    #     for i in range(1, count + 1):
    #         num_func = random.choice(list_func)
    #         num_func(i + message_count)
    #     self.stdout.write(f"Добавлено {count} случайных личных сообщений.")
