from django import conf
from django.utils.functional import classproperty
from django.core.mail import send_mail
from rest_framework import serializers

from accounts.models import FormFieldMetaData
from common.helpers.small import dox_enumes
from main.models import MainMenu


# noinspection PyAbstractClass
class ParadoxDataSerializer(serializers.Serializer):
    """ Сериализатор парадокса дня """
    header = serializers.CharField(max_length=255)
    content = serializers.CharField()


# noinspection PyAbstractClass
class MainSubmenuSerializer(serializers.Serializer):
    """ Сериализатор подменю """
    label = serializers.CharField()
    url = serializers.URLField()


# noinspection PyAbstractClass
class MainMenuSerializer(serializers.Serializer):
    """ Сериализатор меню """
    label = serializers.CharField()
    style = serializers.CharField()
    icon = serializers.CharField()
    url = serializers.URLField()
    is_real = serializers.BooleanField()
    items = MainSubmenuSerializer(many=True)


# noinspection PyAbstractClass
class ContactSerializer(serializers.Serializer):
    """ Сериализатор формы обратной связи """
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True,
                                   error_messages={'required': 'Не заполнен адрес электронной почты',
                                                   'invalid': 'Неправильный адрес электронной почты.'})
    subject = serializers.CharField(max_length=150, required=True)
    message = serializers.CharField()

    @classproperty
    def field_meta_data(self):
        return [
            FormFieldMetaData("username", "id_username", "Логин", dox_enumes.TYPE_TEXT, True,
                              {"maxLength": "100", "minLength": "3"},
                              ("Логин должен быть правильным", "Логин не должен быть пустым",
                               "Логин не должен повторяться")),
            FormFieldMetaData("email", "id_email", "Электронная почта", dox_enumes.TYPE_EMAIL, True),
            FormFieldMetaData("subject", "id_subject", "Тема", dox_enumes.TYPE_TEXT, True),
            FormFieldMetaData("message", "id_message", "Сообщение", dox_enumes.TYPE_TEXTAREA, True,
                              {"cols": "50", "rows": "6"})
            # FormFieldMetaData("verifyCaptcha", "idVerifyCaptcha", "Введите код с картинки", dox_enumes.TYPE_TEXT, True,
            #                   {"autoComplete": "off"}),
        ]

    def send_email(self):
        """ Отправляет вопрос обратной связи по электронной почте """
        username = self.validated_data['username']
        email = self.validated_data['email']
        subject = self.validated_data['subject']
        message = self.validated_data['message']
        from_ = conf.settings.EMAIL_HOST_USER
        at_ = (conf.settings.SERVER_EMAIL,)
        txt_message = f"Тема: {subject}\n" \
                      f"имя отправителя: {username}\n" \
                      f"адрес отправителя: {email}\n" \
                      f"\nСообщение: \n{message}"
        html_message = f'<strong>Тема:</strong> {subject}</br>' \
                       f'<strong>имя отправителя:</strong> {username}</br>' \
                       f'<strong>адрес отправителя:</strong> {email}</br>' \
                       f'<br><strong>Сообщение:</strong> <br>{message}'
        theme = f'Вопрос из формы "Обратной связи" от {username}: {self.validated_data["subject"]}'
        send_mail(theme, txt_message, from_, at_, html_message=html_message)