import pytest

from .mocks import FakeHttpRequest


@pytest.fixture()
def fake_http_request():
    """ Возвращает поддельный HTTP запрос """
    return FakeHttpRequest("/test/sub")


@pytest.fixture()
def fake_http_request_login():
    """ Возвращает поддельный HTTP запрос на страницу логина """
    return FakeHttpRequest("/login")
