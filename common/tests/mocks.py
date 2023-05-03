from rest_framework.request import HttpRequest


class FakeHttpRequest():
    def __init__(self, url: str):
        self._headers = {
            "REMOTE_ADDR": "127.0.0.1,abra-kadabra",
            "Referer": url,
            "User-Agent": "Test no_browser"
        }

    @property
    def headers(self):
        return self._headers
