from common.helpers.small.dox_utils import get_request_ip, get_unique_hash_page


def test_get_request_ip(fake_http_request):
    """ Тестирование получение IP адреса из запроса """
    ip = get_request_ip(fake_http_request)
    assert ip == "127.0.0.1"


def test_get_unique_hash_page(fake_http_request):
    """ Тестирование получения уникального HASH-а URL из запроса """
    unique_id = get_unique_hash_page(fake_http_request)
    assert unique_id == 'bb7b2e3bc9d581285c2b989af1b6a941'


def test_get_unique_hash_page_login(fake_http_request_login):
    """ Тестирование получение постоянного HASH кода страницы /login """
    unique_id = get_unique_hash_page(fake_http_request_login)
    assert unique_id == 1
