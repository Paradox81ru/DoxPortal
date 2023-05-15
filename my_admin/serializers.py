# noinspection PyAbstractClass
from rest_framework import serializers

from accounts.serializers import UserDataSerializer


# noinspection PyAbstractClass
class BeginDataSerializer(serializers.Serializer):
    """ Сериализатор начальных данных для админки """
    breadcrumbList = serializers.JSONField()
    userAuthentication = UserDataSerializer()
