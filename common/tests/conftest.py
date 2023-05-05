import pytest
import os

from .mocks import FakeHttpRequest


@pytest.fixture()
def fake_http_request():
    """ Возвращает поддельный HTTP запрос """
    return FakeHttpRequest("/test/sub")


@pytest.fixture()
def fake_http_request_login():
    """ Возвращает поддельный HTTP запрос на страницу логина """
    return FakeHttpRequest("/login")


@pytest.fixture()
def destination_file(tmp_path):
    """ Создаёт временный файл и возвращает путь к нему """
    filename = os.path.join(tmp_path, "destination_file.jpg")
    open(filename, 'a').close()
    return filename


@pytest.fixture()
def patched_constant_debug(monkeypatch):
    """ Патчит константу DEBUG """
    monkeypatch.setattr("django.conf.settings.DEBUG", True)
    return True

@pytest.fixture()
def patched_constant_test_captcha(monkeypatch):
    """ Патчит константу TEST_CAPTCHA """
    monkeypatch.setattr("django.conf.settings.TEST_CAPTCHA", True)
    return True
