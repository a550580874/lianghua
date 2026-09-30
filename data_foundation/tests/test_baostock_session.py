from types import SimpleNamespace

from data_foundation.baostock_session import BaoStockSessionManager


class StubClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.login_calls = 0
        self.logout_calls = 0
        self.request_calls = 0

    def login(self):
        self.login_calls += 1
        return SimpleNamespace(error_code="0", error_msg="success")

    def logout(self):
        self.logout_calls += 1

    def query(self):
        self.request_calls += 1
        return self.responses.pop(0)


def response(code, message=""):
    return SimpleNamespace(error_code=code, error_msg=message)


def test_session_expired_reconnects_and_retries_without_leaking_token():
    client = StubClient([response("10001001", "用户未登录"), response("0", "ok")])
    sleeps = []
    manager = BaoStockSessionManager(client, sleep=sleeps.append)

    result = manager.request(client.query)

    assert result.error_code == "0"
    assert client.login_calls == 2
    assert client.logout_calls == 1
    assert client.request_calls == 2
    assert sleeps == [1]


def test_retry_limit_returns_last_transient_response():
    client = StubClient([response("10001001", "用户未登录") for _ in range(4)])
    sleeps = []
    manager = BaoStockSessionManager(client, max_retries=3, sleep=sleeps.append)

    result = manager.request(client.query)

    assert result.error_code == "10001001"
    assert client.request_calls == 4
    assert client.login_calls == 4
    assert sleeps == [1, 2, 4]


def test_refresh_interval_reconnects_before_request():
    now = [0.0]
    client = StubClient([response("0", "ok")])
    manager = BaoStockSessionManager(client, refresh_interval_seconds=10, clock=lambda: now[0])
    manager.login()
    now[0] = 10.0

    manager.request(client.query)

    assert client.login_calls == 2
    assert client.logout_calls == 1
