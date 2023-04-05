from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Paradox, get_breadcrumb_list, get_main_menu_list, get_main_menu
from accounts.models import User
from accounts.serializers import FormFieldMetaDataSerializer
from common.serializers import BeginDataSerializer


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
def get_login_form_data(request):
    login_form_field_meta_data_serializer = FormFieldMetaDataSerializer(User.field_meta_data, many=True)
    return Response(login_form_field_meta_data_serializer.data)
