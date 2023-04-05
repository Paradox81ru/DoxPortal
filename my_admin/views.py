from django.shortcuts import render


def main(request):
    """ Главная страница"""
    return render(request, 'my_admin/index.html')
