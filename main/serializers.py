from rest_framework import serializers
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
