from rest_framework import serializers

from .models import User


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


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
