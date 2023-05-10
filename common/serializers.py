from django.utils.functional import classproperty
from rest_framework import serializers

from accounts.models import FormFieldMetaData
from common.helpers.small import dox_enumes
from main.serializers import ParadoxDataSerializer, MainMenuSerializer
from accounts.serializers import UserDataSerializer
from main.models import Paradox


# noinspection PyAbstractClass
class BeginDataSerializer(serializers.Serializer):
    """ Сериализатор начальных данных """
    paradoxData = ParadoxDataSerializer()
    breadcrumbList = serializers.JSONField()
    userAuthentication = UserDataSerializer()
    mainMenu = MainMenuSerializer(many=True)
    currentYear = serializers.IntegerField()
    siteDomainName = serializers.URLField()
    isShowCaptcha = serializers.BooleanField()


# noinspection PyAbstractClass
class LoginSerializer(serializers.Serializer):
    """ Сериализатор данных при логировании """
    userAuthentication = UserDataSerializer()
    token = serializers.CharField()
    mainMenu = MainMenuSerializer(many=True)


# noinspection PyAbstractClass
class RegisterUserSerializer(serializers.Serializer):
    """ Сериализатор данных регистрации нового пользователя """
    username = serializers.CharField(label="username", min_length=3, max_length=150, required=True)
    email = serializers.EmailField(label="email", required=True,
                                   error_messages={'required': 'Не заполнен адрес электронной почты',
                                                   'invalid': 'Неправильный адрес электронной почты.'})
    password = serializers.CharField(label="password", required=True)
    passwordConfirm = serializers.CharField(label="passwordConfirm", required=True)

    @classproperty
    def field_meta_data(self):
        return [
            FormFieldMetaData("username", "id_username", "Логин", dox_enumes.TYPE_TEXT, True,
                              {"maxLength": "100", "minLength": "3"},
                              ("Логин должен состоять только из букв латинского алфавита, цифр, подчеркивания и дефиса.",
                               "Логин должен содержать не менее 3 и не более 100 символов.",
                               "Логин не может начинаться или завершаться с дефиса или подчеркивания, а так же запрещены любые комбинации подчеркивания и дефиса.",
                               "Логин не должен быть похожим на логины 'admin', 'paradox' или 'system'.")),
            FormFieldMetaData("email", "id_email", "Электронная почта", dox_enumes.TYPE_EMAIL, True),
            FormFieldMetaData("password", "id_password", "Пароль", dox_enumes.TYPE_TEXT, True, None,
                              ("Ваш пароль не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё.",
                               "Ваш пароль должен содержать не менее 6 символов, как минимум 1 цифру, как минимум 1 букву в верхнем регистре и 1 букву в нижнем регистре, и как минимум один знак.",
                               "Ваш пароль не может быть одним из широко распространённых паролей.",
                               "Ваш пароль не может состоять только из цифр.")),
            FormFieldMetaData("passwordConfirm", "id_passwordConfirm", "Подтверждение пароля", dox_enumes.TYPE_TEXT,
                              True, None,
                              ("Для подтверждения введите, пожалуйста, пароль ещё раз.",))
        ]


# noinspection PyAbstractClass
class FormFieldMetaDataSerializer(serializers.Serializer):
    fieldName = serializers.CharField()
    id = serializers.CharField()
    label = serializers.CharField()
    fieldType = serializers.CharField()
    isRequired = serializers.BooleanField()
    inputAttributes = serializers.DictField()
    helper = serializers.ListField()
    valueList = serializers.ListField()