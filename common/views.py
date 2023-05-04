from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from main.models import Paradox, get_breadcrumb_list, get_main_menu_list, get_main_menu
from accounts.models import User
from common.serializers import FormFieldMetaDataSerializer
from main.serializers import ContactSerializer
from common.serializers import BeginDataSerializer
from common.helpers.big.dox_captcha.captcha_service import CaptchaService

@api_view(['GET'])
def get_begin_data(request):
    """ Возвращает начальные данные для загрузки интерфейса """
    user = request.user
    if user.is_anonymous:
        user.email = ""
    begin_data_serializer = BeginDataSerializer({
        'paradoxData': Paradox.objects.rnd_paradox,
        'breadcrumbList': get_breadcrumb_list(),
        'userAuthentication': user,
        'mainMenu': get_main_menu_list(user),
        'currentYear': timezone.now().year,
        'siteDomainName': request.get_host(),
        'isShowCaptcha': False
    })
    return Response(begin_data_serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_login_form_data(request):
    """ Возвращает данные для формы страницы авторизации """
    login_form_field_meta_data_serializer = FormFieldMetaDataSerializer(User.field_meta_data, many=True)
    return Response(login_form_field_meta_data_serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_contact_form_data(request):
    contact_form_field_meta_data_serializer = FormFieldMetaDataSerializer(ContactSerializer.field_meta_data, many=True)
    return Response(contact_form_field_meta_data_serializer.data)


class AboutPageView(APIView):
    """ Возвращает статические данные для страницы "О сайте" """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/fragments/about.html"

    def get(self, request):
        return Response()


class ContactView(APIView):
    """ Отправляет форму обратной связи """
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            if not CaptchaService().validate_captcha_request(serializer.data.get("verifyCaptcha"), request):
                error_data = {"error": "VerifyCaptchaError", "data": {"verifyCaptcha": ["Неверный код"]}}
                return Response(error_data)
            # serializer.send_email()
            return Response({"success": "Ok"})
        else:
            error_data = {"error": "FieldValidateError", "data": serializer.errors}
            return Response(error_data)
