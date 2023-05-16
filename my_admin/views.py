from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import get_admin_breadcrumb_list
from my_admin.serializers import BeginDataSerializer


def main(request):
    """ Главная страница"""
    return render(request, 'my_admin/index.html')


@api_view(["GET"])
def begin_data(request):
    user = request.user
    if user.is_anonymous:
        user.email = ""
    begin_data_serializer = BeginDataSerializer({
        'breadcrumbList': get_admin_breadcrumb_list(),
        'userAuthentication': user,
    })
    return Response(begin_data_serializer.data)
