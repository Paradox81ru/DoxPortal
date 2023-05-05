from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers

from common.helpers.big.dox_captcha.captcha_service import CaptchaService


class DoxAuthTokenSerializer(AuthTokenSerializer):
    verifyCaptcha = serializers.CharField(label="VerifyCaptcha", allow_blank=True)

    def validate_verifyCaptcha(self, value):
        captcha_service = CaptchaService()
        request = self.context.get("request")
        if captcha_service.is_show_captcha(request):
            if captcha_service.validate_captcha(value, request):
                return value
            else:
                raise serializers.ValidationError("Неверный код")
        return value
