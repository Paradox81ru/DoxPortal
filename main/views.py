from django.http import HttpResponse
from django.shortcuts import render

from common.helpers.big.dox_captcha.captcha import Captcha


def main(request):
    return render(request, 'main/index.html')


def main_path(request, path):
    return render(request, 'main/index.html')


# noinspection PyUnusedLocal
def captcha_v(request, rand=None):
    if request.method == 'GET':
        response = HttpResponse(content_type="image/png")
        if request.session.get('captcha', None):
            del request.session['captcha']
        captcha = Captcha(response)
        request.session['captcha'] = captcha()
        return response
