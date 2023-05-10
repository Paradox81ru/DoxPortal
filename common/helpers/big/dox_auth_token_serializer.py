from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.helpers.big.dox_captcha.captcha_service import CaptchaService


# noinspection PyAbstractClass
class DoxAuthTokenSerializer(AuthTokenSerializer):
    verifyCaptcha = serializers.CharField(label="VerifyCaptcha", allow_blank=True)

    # noinspection PyPep8Naming
    def validate_verifyCaptcha(self, value):
        captcha_service = CaptchaService()
        request = self.context.get("request")
        if captcha_service.is_show_captcha(request):
            if captcha_service.validate_captcha(value, request):
                return value
            else:
                raise serializers.ValidationError("Неверный код", code="captcha")
        return value

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except serializers.ValidationError as er:
            CaptchaService().add_failure_validate(self.context.get("request"))
            raise serializers.ValidationError(er.detail, code='authorization')