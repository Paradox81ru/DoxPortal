from django.shortcuts import render


def main(request):
    return render(request, 'main/index.html')


def main_path(request, path):
    return render(request, 'main/index.html')