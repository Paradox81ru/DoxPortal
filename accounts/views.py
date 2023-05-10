from django.contrib.auth.signals import user_logged_in

from rest_framework.response import Response
from rest_framework.views import APIView

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.authentication import BasicAuthentication

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render

from common.permissions import OnlyAdminPermission
from accounts.serializers import LoginSerializer, RegisterUserSerializer
from accounts.models import User
from main.models import get_main_menu_list
from common.helpers.big.dox_captcha.captcha_service import CaptchaService
from common.helpers.big.dox_auth_token_serializer import DoxAuthTokenSerializer
from .serializers import UserDataSerializer

# class LoginView(KnoxLoginView):
#     authentication_classes = [BasicAuthentication]


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def _get_token(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        return token

    def post(self, request, format=None):
        serializer = DoxAuthTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token = self._get_token(request, format)
        login_serializer = LoginSerializer({
            'userAuthentication': user,
            'token': token,
            'mainMenu': get_main_menu_list(user),
        })
        return Response(login_serializer.data)


class Signup(APIView):
    """ Регистрация новой учётной записи """
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": "Ok"})
        else:
            error_data = {"error": "FieldValidateError", "fields_error": serializer.errors}
            return Response(error_data)


class GetAllUsers(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        #  Получаем набор всех записей из таблицы User
        queryset = User.objects.all()
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = UserDataSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class GetAdmin(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyAdminPermission, )

    def get(self, request):
        admin = User.objects.get(username="Admin")
        serializer = UserDataSerializer(instance=admin)
        return Response(serializer.data)


class GetUser(APIView):
    def get(self, request):
        user = User.objects.get(username="User")
        serializer = UserDataSerializer(instance=user)
        return Response(serializer.data)
