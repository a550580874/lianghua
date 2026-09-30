import unittest
from types import SimpleNamespace
from data_foundation.baostock_session import BaoStockSessionManager

class Client:
    def __init__(self): self.n=0
    def login(self): return SimpleNamespace(error_code='0',error_msg='')
    def logout(self): pass
    def query(self):
        self.n+=1
        return SimpleNamespace(error_code='10001001' if self.n==1 else '0', error_msg='用户未登录' if self.n==1 else '')

class SessionTests(unittest.TestCase):
    def test_reconnect_retry(self):
        c=Client(); m=BaoStockSessionManager(c,sleep=lambda _:None); m.login(); self.assertEqual(m.request(c.query).error_code,'0')
    def test_retry_limit(self):
        c=Client(); c.query=lambda: SimpleNamespace(error_code='10001001',error_msg='用户未登录'); m=BaoStockSessionManager(c,sleep=lambda _:None,max_retries=2); m.login(); self.assertEqual(m.request(c.query).error_code,'10001001')
