from rest_framework import serializers

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
class FormFieldMetaDataSerializer(serializers.Serializer):
    fieldName = serializers.CharField()
    id = serializers.CharField()
    label = serializers.CharField()
    fieldType = serializers.CharField()
    isRequired = serializers.BooleanField()
    inputAttributes = serializers.DictField()
    helper = serializers.ListField()
    valueList = serializers.ListField()