from django.db import models
from rest_framework.permissions import BasePermission


class Permission(models.Model):
    """ Вирутальная модель для создания разрешений для администрирования сайта """
    can_see_menu_admin = 'my_admin.see_menu_admin'
    can_open_menu_admin = 'my_admin.open_menu_admin'

    class Meta:
        # Благодаря этому база данных создана не будет.
        managed = False
        verbose_name = "Разрешение"
        verbose_name_plural = "Разрешения"
        default_permissions = ()
        permissions = [
            ('see_menu_admin', 'Может видеть меню администратора'),
            ('open_menu_admin', 'Может открыть меню администратора'),
        ]

