from django.utils.functional import classproperty
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from common.helpers.small import dox_enumes
from common.helpers.small.mixins import MixinSerializerValidateUsernameAndEmail
from main.serializers import MainMenuSerializer
from .models import User, FormFieldMetaData


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


# noinspection PyAbstractClass
class LoginSerializer(serializers.Serializer):
    """ Сериализатор данных при логировании """
    userAuthentication = UserDataSerializer()
    userGroups = serializers.ListField()
    token = serializers.CharField()
    mainMenu = MainMenuSerializer(many=True)


# noinspection PyAbstractClass
class RegisterUserSerializer(MixinSerializerValidateUsernameAndEmail, serializers.ModelSerializer):
    """ Сериализатор данных регистрации нового пользователя """
    passwordConfirm = serializers.CharField(label="Подтверждение пароля", required=True,
                                            help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "password", "passwordConfirm")

    def validate(self, attrs: dict):
        password = attrs.get("password")
        password_confirm = attrs.get("passwordConfirm")
        if password and password_confirm and password_confirm != password:
            raise serializers.ValidationError({"passwordConfirm": "Пароли не совпадают"}, code='password_mismatch')

        return attrs

    @classproperty
    def field_meta_data(self):
        return [
            FormFieldMetaData("username", "id_username", "Логин", dox_enumes.TYPE_TEXT, True,
                              {"maxLength": "100", "minLength": "3"},
                              ("Логин должен состоять только из букв латинского алфавита, цифр, "
                                          "подчеркивания и дефиса.",
                                          "Логин должен содержать не менее 3 и не более 100 символов.",
                                          "Логин не может начинаться или завершаться с дефиса или подчеркивания.",
                                          "Логин не должен быть похожим на логины 'admin', 'paradox' или 'system'.")),
            FormFieldMetaData("email", "id_email", "Электронная почта", dox_enumes.TYPE_EMAIL, True),
            FormFieldMetaData("password", "id_password", "Пароль", dox_enumes.TYPE_TEXT, True, {"autoComplete": "off"},
                              ("Ваш пароль не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё.",
                               "Ваш пароль должен содержать не менее 6 символов, как минимум 1 цифру, как минимум 1 букву в верхнем регистре и 1 букву в нижнем регистре, и как минимум один знак.",
                               "Ваш пароль не может быть одним из широко распространённых паролей.",
                               "Ваш пароль не может состоять только из цифр.")),
            FormFieldMetaData("passwordConfirm", "id_passwordConfirm", "Подтверждение пароля", dox_enumes.TYPE_TEXT,
                              True, {"autoComplete": "off"},
                              ("Для подтверждения введите, пожалуйста, пароль ещё раз.",))
        ]
