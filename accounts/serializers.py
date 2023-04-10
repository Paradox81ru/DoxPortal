from rest_framework import serializers

from .models import User


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

