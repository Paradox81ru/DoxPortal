import re

from rest_framework import serializers

from accounts.models import User


# noinspection PyUnresolvedReferences
class MixinSerializerValidateUsernameAndEmail:
    """ Миксин позволяющий производить проверку сериализации на правильность и уникальность ввода username и email """
    def validate_username(self, value):
        # noinspection PyUnresolvedReferences
        username = value
        username = re.sub('_{2,}', '_', username)   # убирает двойные подчеркивания
        username = re.sub('-{2,}', '-', username)   # убирает двойные дефисы
        username = username.replace('-_', '_')
        username = username.replace('_-', '-')
        pattern1 = re.compile(r"[^a-zA-Z0-9_-]")    # разрешим только буквы лат. алфавита, цифры, дефис и подчеркивание
        pattern2 = re.compile(r"(^[-_]+|[-_]+$)")   # запретим подчеркивание и дефисы в начале и в конце
        pattern3 = re.compile(r"^(.{0,2}[_-]+)?admin([_-]+.{0,2})?$", re.IGNORECASE)    # запретим логины схожие с admin
        pattern4 = re.compile(r"^(.{0,2}[_-]+)?paradox([_-]+.{0,2})?$", re.IGNORECASE)  # запретим логины схожие с paradox
        pattern5 = re.compile(r"^(.{0,2}[_-]+)?system([_-]+.{0,2})?$", re.IGNORECASE)  # запретим логины схожие с system
        if pattern1.search(username) is not None \
                or pattern2.search(username) is not None \
                or pattern3.search(username) is not None \
                or pattern4.search(username) is not None \
                or pattern5.search(username) is not None:
            raise serializers.ValidationError("Такой логин запрещен.",code="invalid")
        else:
            check_unique = User.objects.check_unique_username(username)
            if check_unique == 1:
                raise serializers.ValidationError(
                    "Такой логин уже существует.",
                    code="not_unique"
                )
            elif check_unique == 2:
                raise serializers.ValidationError(
                    "Этот логин уже ждет подтверждения.",
                    code="wait_confirm"
                )
        return username

    def validate_email(self, value):
        # noinspection PyUnresolvedReferences
        email = value.lower()
        check_unique = User.objects.check_unique_email(email)
        if check_unique == 1:
            raise serializers.ValidationError(
                "Такой адрес электронной почты уже используется.",
                code="not_unique"
            )
        elif check_unique == 2:
            raise serializers.ValidationError(
                "Такой адрес электронной почты уже ждет подтверждения.",
                code="wait_confirm"
            )
        return email
